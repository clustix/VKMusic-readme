from colors import get_dominant_colors, image_to_base64, rgb_to_hex, FALLBACK_COLORS


def truncate(text, max_chars):
    return text if len(text) <= max_chars else text[:max_chars - 1] + '…'


def generate_svg(artist, title, cover_url, is_now_playing=True):
    if cover_url:
        colors = get_dominant_colors(cover_url)
        hex_accent = rgb_to_hex(colors[0])
    else:
        hex_accent = '#4ade80'

    bg_color = "#0e0e11"
    card_border = "rgba(255, 255, 255, 0.08)"

    cover_b64 = image_to_base64(cover_url) if cover_url else None

    if cover_b64:
        cover_block = f'<image href="{cover_b64}" x="12" y="12" width="96" height="96" clip-path="url(#cover-clip)" preserveAspectRatio="xMidYMid slice"/>'
    else:
        cover_block = f'<rect x="12" y="12" width="96" height="96" rx="8" fill="#18181b"/><text x="60" y="66" text-anchor="middle" font-size="36" font-family="system-ui, -apple-system, sans-serif" fill="#71717a">♫</text>'

    title_safe = truncate(title, 28) if title else 'Ничего не играет'
    artist_safe = truncate(artist, 32) if artist else ''
    
    label = 'СЕЙЧАС ИГРАЕТ' if is_now_playing else 'ПОСЛЕДНИЙ ТРЕК'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="480" height="120">
  <defs>
    <clipPath id="cover-clip">
      <rect x="12" y="12" width="96" height="96" rx="8"/>
    </clipPath>
    <clipPath id="card-clip">
      <rect width="480" height="120" rx="14"/>
    </clipPath>
    <style>
      @keyframes wm   {{ 0%{{transform:translateX(0)}}   100%{{transform:translateX(-50%)}} }}
      @keyframes wm2  {{ 0%{{transform:translateX(0)}}   100%{{transform:translateX(50%)}}  }}
      @keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:0.4}} }}
      .wa {{ animation: wm  6s linear infinite; }}
      .wb {{ animation: wm2 9s linear infinite; }}
      .ring {{ animation: pulse 2s ease-in-out infinite; }}
    </style>
  </defs>

  <rect width="480" height="120" rx="14" fill="{bg_color}" stroke="{card_border}" stroke-width="1"/>

  <g clip-path="url(#card-clip)">
    <g class="wa"><path fill="rgba(255,255,255,0.03)" d="M0,95 C60,82 120,108 180,95 C240,82 300,108 360,95 C420,82 480,108 540,95 C600,82 660,108 720,95 L720,120 L0,120 Z"/></g>
    <g class="wb"><path fill="rgba(255,255,255,0.02)" d="M0,102 C80,90 160,114 240,102 C320,90 400,114 480,102 C560,90 640,114 720,102 L720,120 L0,120 Z"/></g>
  </g>

  {cover_block}
  <rect x="12" y="12" width="96" height="96" rx="8" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>

  <text x="124" y="36" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="rgba(255,255,255,0.4)" font-weight="600" letter-spacing="1.5">{label}</text>
  <text x="124" y="60" font-family="system-ui, -apple-system, sans-serif" font-size="16" fill="#f4f4f5" font-weight="700">{title_safe}</text>
  <text x="124" y="80" font-family="system-ui, -apple-system, sans-serif" font-size="13" fill="#a1a1aa">{artist_safe}</text>

  <rect x="124" y="96" width="220" height="3" rx="1.5" fill="rgba(255,255,255,0.08)"/>
  <rect x="124" y="96" width="90" height="3" rx="1.5" fill="{hex_accent}"/>

  <circle class="ring" cx="415" cy="60" r="26" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <circle cx="415" cy="60" r="20" fill="rgba(255,255,255,0.08)"/>
  <polygon points="410,51 410,69 426,60" fill="#f4f4f5"/>
</svg>'''
