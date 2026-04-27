// TubeFlow — YouTube channel automation desktop app
// Dark SaaS aesthetic, sidebar nav + 4 main tabs

const { useState, useEffect, useRef, useMemo } = React;

// ─────────────────────────────────────────────────────────────
// Design tokens
// ─────────────────────────────────────────────────────────────
const T = {
  bg:        '#0E1014',          // deepest charcoal
  panel:     '#15181F',          // sidebar / cards base
  panel2:    '#1B1F27',          // raised cards
  panel3:    '#22262F',          // hover / inputs
  border:    '#262A33',
  borderHi:  '#333845',
  text:      '#E7E9EE',
  textDim:   '#9097A3',
  textMute:  '#5C6370',
  accent:    '#FF4655',          // coral red — youtube-adjacent but distinct
  accentDim: '#3A1A1F',
  accentHi:  '#FF6B78',
  green:     '#3DD68C',
  amber:     '#F5B544',
  blue:      '#5B9CFF',
  font:      '"Inter", -apple-system, "Segoe UI", "Pretendard", sans-serif',
  mono:      '"JetBrains Mono", "SF Mono", ui-monospace, monospace',
};

// ─────────────────────────────────────────────────────────────
// Tiny stroke icons (1.5px) — original geometry, no brand glyphs
// ─────────────────────────────────────────────────────────────
function Icon({ name, size = 16, color = 'currentColor' }) {
  const s = { width: size, height: size, stroke: color, fill: 'none', strokeWidth: 1.5, strokeLinecap: 'round', strokeLinejoin: 'round' };
  switch (name) {
    case 'collect': return (
      <svg viewBox="0 0 20 20" {...s}>
        <path d="M3 6h14M3 10h14M3 14h9" />
        <circle cx="16" cy="14" r="2.2" />
      </svg>
    );
    case 'script': return (
      <svg viewBox="0 0 20 20" {...s}>
        <path d="M5 3h8l3 3v11a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z" />
        <path d="M13 3v3h3M7 11h6M7 14h4" />
      </svg>
    );
    case 'upload': return (
      <svg viewBox="0 0 20 20" {...s}>
        <rect x="3" y="5" width="14" height="11" rx="2" />
        <path d="M10 12V8M8 10l2-2 2 2" />
      </svg>
    );
    case 'trend': return (
      <svg viewBox="0 0 20 20" {...s}>
        <path d="M3 14l4-4 3 2 7-7" />
        <path d="M12 5h5v5" />
      </svg>
    );
    case 'settings': return (
      <svg viewBox="0 0 20 20" {...s}>
        <circle cx="10" cy="10" r="2.5" />
        <path d="M10 2v2M10 16v2M2 10h2M16 10h2M4.3 4.3l1.4 1.4M14.3 14.3l1.4 1.4M4.3 15.7l1.4-1.4M14.3 5.7l1.4-1.4" />
      </svg>
    );
    case 'play': return (
      <svg viewBox="0 0 20 20" {...s} fill={color}>
        <path d="M6 4l10 6-10 6V4z" />
      </svg>
    );
    case 'search': return (
      <svg viewBox="0 0 20 20" {...s}>
        <circle cx="9" cy="9" r="5.5" />
        <path d="M13 13l3.5 3.5" />
      </svg>
    );
    case 'plus': return <svg viewBox="0 0 20 20" {...s}><path d="M10 4v12M4 10h12" /></svg>;
    case 'check': return <svg viewBox="0 0 20 20" {...s}><path d="M4 10l4 4 8-9" /></svg>;
    case 'clock': return (
      <svg viewBox="0 0 20 20" {...s}>
        <circle cx="10" cy="10" r="7" />
        <path d="M10 6v4l3 2" />
      </svg>
    );
    case 'arrow-up': return <svg viewBox="0 0 20 20" {...s}><path d="M10 16V4M5 9l5-5 5 5" /></svg>;
    case 'arrow-down': return <svg viewBox="0 0 20 20" {...s}><path d="M10 4v12M5 11l5 5 5-5" /></svg>;
    case 'dot': return <svg viewBox="0 0 20 20"><circle cx="10" cy="10" r="3.5" fill={color} /></svg>;
    case 'spark': return (
      <svg viewBox="0 0 20 20" {...s}>
        <path d="M10 3l1.6 4.4L16 9l-4.4 1.6L10 15l-1.6-4.4L4 9l4.4-1.6L10 3z" />
      </svg>
    );
    case 'image': return (
      <svg viewBox="0 0 20 20" {...s}>
        <rect x="3" y="4" width="14" height="12" rx="1.5" />
        <circle cx="7" cy="8" r="1.2" />
        <path d="M3 13l4-3 4 3 3-2 3 2" />
      </svg>
    );
    case 'video': return (
      <svg viewBox="0 0 20 20" {...s}>
        <rect x="2" y="5" width="12" height="10" rx="1.5" />
        <path d="M14 9l4-2v6l-4-2z" />
      </svg>
    );
    case 'calendar': return (
      <svg viewBox="0 0 20 20" {...s}>
        <rect x="3" y="4" width="14" height="13" rx="1.5" />
        <path d="M3 8h14M7 3v3M13 3v3" />
      </svg>
    );
    case 'reddit': return (
      <svg viewBox="0 0 20 20" {...s}>
        <circle cx="10" cy="11" r="6" />
        <circle cx="10" cy="3.5" r="1.2" />
        <path d="M14.5 7.5l-1.5-4" />
        <circle cx="7.5" cy="11" r="0.6" fill={color} />
        <circle cx="12.5" cy="11" r="0.6" fill={color} />
        <path d="M7.5 13.5c.8.6 1.6.9 2.5.9s1.7-.3 2.5-.9" />
      </svg>
    );
    case 'chevron-down': return <svg viewBox="0 0 20 20" {...s}><path d="M5 8l5 5 5-5" /></svg>;
    case 'folder': return (
      <svg viewBox="0 0 20 20" {...s}>
        <path d="M3 6a1 1 0 0 1 1-1h4l2 2h6a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V6z" />
      </svg>
    );
    case 'trash': return (
      <svg viewBox="0 0 20 20" {...s}>
        <path d="M4 6h12M8 6V4h4v2M6 6l1 10h6l1-10" />
      </svg>
    );
    case 'edit': return (
      <svg viewBox="0 0 20 20" {...s}>
        <path d="M4 14l-1 3 3-1 9-9-2-2-9 9z" />
        <path d="M12 4l3 3" />
      </svg>
    );
    case 'eye': return (
      <svg viewBox="0 0 20 20" {...s}>
        <path d="M2 10s3-5 8-5 8 5 8 5-3 5-8 5-8-5-8-5z" />
        <circle cx="10" cy="10" r="2.5" />
      </svg>
    );
    case 'thumbs-up': return (
      <svg viewBox="0 0 20 20" {...s}>
        <path d="M3 9h3v8H3zM6 9l3-6c1.5 0 2.5 1 2.5 2.5V8h4a1.5 1.5 0 0 1 1.5 1.7l-1 6A1.5 1.5 0 0 1 14.5 17H6" />
      </svg>
    );
    case 'globe': return (
      <svg viewBox="0 0 20 20" {...s}>
        <circle cx="10" cy="10" r="7" />
        <path d="M3 10h14M10 3c2.5 2.8 2.5 11.2 0 14M10 3c-2.5 2.8-2.5 11.2 0 14" />
      </svg>
    );
    default: return null;
  }
}

// ─────────────────────────────────────────────────────────────
// Window chrome
// ─────────────────────────────────────────────────────────────
function TrafficLights() {
  const dot = (bg) => <div style={{ width: 12, height: 12, borderRadius: '50%', background: bg, border: '0.5px solid rgba(0,0,0,0.25)' }} />;
  return (
    <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
      {dot('#ff5f57')}{dot('#febc2e')}{dot('#28c840')}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
// Sidebar
// ─────────────────────────────────────────────────────────────
const NAV = [
  { id: 'collect',  label: '소재 수집',   icon: 'collect',  hint: 'Collect' },
  { id: 'script',   label: '대본 작성',   icon: 'script',   hint: 'Script'  },
  { id: 'upload',   label: '업로드 예약', icon: 'upload',   hint: 'Upload'  },
  { id: 'trend',    label: '트렌드 분석', icon: 'trend',    hint: 'Trends'  },
];

function Sidebar({ tab, setTab, server, setServer }) {
  return (
    <div style={{
      width: 232, flexShrink: 0,
      background: T.panel, borderRight: `1px solid ${T.border}`,
      display: 'flex', flexDirection: 'column',
    }}>
      {/* logo row — sits next to traffic lights */}
      <div style={{ height: 44, display: 'flex', alignItems: 'center', padding: '0 16px', gap: 12 }}>
        <TrafficLights />
      </div>

      <div style={{ padding: '4px 16px 18px', display: 'flex', alignItems: 'center', gap: 10 }}>
        <div style={{
          width: 28, height: 28, borderRadius: 8, background: T.accent,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          boxShadow: `0 4px 14px ${T.accent}55`,
        }}>
          <Icon name="play" size={13} color="#fff" />
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', lineHeight: 1.1 }}>
          <span style={{ color: T.text, fontWeight: 700, fontSize: 14, letterSpacing: '-0.01em' }}>TubeFlow</span>
          <span style={{ color: T.textMute, fontSize: 11, fontFamily: T.mono }}>v0.4.2 · local</span>
        </div>
      </div>

      <div style={{ padding: '0 10px 0 10px', display: 'flex', flexDirection: 'column', gap: 2 }}>
        <SidebarSection label="WORKSPACE" />
        {NAV.map(n => (
          <NavItem key={n.id} active={tab === n.id} onClick={() => setTab(n.id)} icon={n.icon} label={n.label} hint={n.hint} />
        ))}

        <SidebarSection label="LIBRARY" style={{ marginTop: 18 }} />
        <NavItem icon="folder" label="저장된 소재" hint="32" muted />
        <NavItem icon="folder" label="생성된 대본" hint="14" muted />
        <NavItem icon="folder" label="업로드 큐"   hint="3"  muted />
      </div>

      <div style={{ flex: 1 }} />

      {/* server status */}
      <div style={{ padding: '12px 14px', borderTop: `1px solid ${T.border}` }}>
        <div style={{ fontSize: 10, fontWeight: 600, letterSpacing: '0.08em', color: T.textMute, marginBottom: 8 }}>SERVER</div>
        <div style={{ display: 'flex', background: T.panel2, borderRadius: 8, padding: 3, border: `1px solid ${T.border}` }}>
          {['local', 'team'].map(k => (
            <button key={k} onClick={() => setServer(k)} style={{
              flex: 1, padding: '6px 8px', fontSize: 11, fontWeight: 600,
              border: 'none', cursor: 'pointer',
              background: server === k ? T.panel3 : 'transparent',
              color: server === k ? T.text : T.textDim,
              borderRadius: 6, fontFamily: T.font,
              textTransform: 'capitalize',
            }}>{k === 'local' ? '로컬' : '팀'}</button>
          ))}
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 10, fontSize: 11, color: T.textDim }}>
          <span style={{
            width: 6, height: 6, borderRadius: '50%', background: T.green,
            boxShadow: `0 0 8px ${T.green}`,
          }} />
          {server === 'local' ? '127.0.0.1:8421' : 'team-1.tubeflow.io'}
          <span style={{ marginLeft: 'auto', fontFamily: T.mono, color: T.textMute }}>42ms</span>
        </div>
      </div>

      {/* settings */}
      <div style={{ padding: '8px 10px 12px' }}>
        <NavItem icon="settings" label="설정" hint="⌘," />
      </div>
    </div>
  );
}

function SidebarSection({ label, style }) {
  return (
    <div style={{
      padding: '10px 10px 4px', fontSize: 10, fontWeight: 700,
      letterSpacing: '0.1em', color: T.textMute, ...style,
    }}>{label}</div>
  );
}

function NavItem({ active, onClick, icon, label, hint, muted }) {
  const [hover, setHover] = useState(false);
  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        display: 'flex', alignItems: 'center', gap: 10,
        padding: '7px 10px', borderRadius: 7,
        background: active ? T.panel3 : (hover ? '#1A1D24' : 'transparent'),
        border: 'none', cursor: 'pointer',
        color: active ? T.text : (muted ? T.textDim : T.text),
        fontSize: 13, fontWeight: active ? 600 : 500, fontFamily: T.font,
        textAlign: 'left', position: 'relative',
        transition: 'background 80ms ease',
      }}>
      {active && (
        <span style={{
          position: 'absolute', left: -10, top: 6, bottom: 6, width: 2,
          background: T.accent, borderRadius: 2,
        }} />
      )}
      <Icon name={icon} size={16} color={active ? T.accent : (muted ? T.textMute : T.textDim)} />
      <span style={{ flex: 1 }}>{label}</span>
      {hint && (
        <span style={{
          fontSize: 10, color: T.textMute, fontFamily: T.mono,
          padding: muted ? '1px 6px' : 0,
          background: muted ? T.panel2 : 'transparent',
          borderRadius: 4,
        }}>{hint}</span>
      )}
    </button>
  );
}
