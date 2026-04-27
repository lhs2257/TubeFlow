// Shared UI primitives — Button, Input, Select, Card, Tag, etc.

function Button({ children, variant = 'primary', size = 'md', icon, onClick, disabled, style = {} }) {
  const [hover, setHover] = useState(false);
  const sizes = {
    sm: { h: 28, fs: 12, px: 10, gap: 6, ic: 13 },
    md: { h: 34, fs: 13, px: 14, gap: 8, ic: 15 },
    lg: { h: 40, fs: 14, px: 18, gap: 8, ic: 16 },
  };
  const sz = sizes[size];
  const styles = {
    primary: {
      background: hover ? T.accentHi : T.accent,
      color: '#fff', border: 'none',
      boxShadow: `0 1px 0 rgba(255,255,255,0.15) inset, 0 4px 14px ${T.accent}40`,
    },
    secondary: {
      background: hover ? T.panel3 : T.panel2,
      color: T.text, border: `1px solid ${hover ? T.borderHi : T.border}`,
    },
    ghost: {
      background: hover ? T.panel2 : 'transparent',
      color: T.textDim, border: 'none',
    },
    danger: {
      background: hover ? '#3A1A1F' : 'transparent',
      color: T.accent, border: `1px solid ${T.accentDim}`,
    },
  };
  return (
    <button onClick={onClick} disabled={disabled}
      onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
      style={{
        height: sz.h, padding: `0 ${sz.px}px`, fontSize: sz.fs,
        display: 'inline-flex', alignItems: 'center', gap: sz.gap,
        borderRadius: 7, fontWeight: 600, fontFamily: T.font,
        cursor: disabled ? 'not-allowed' : 'pointer',
        opacity: disabled ? 0.5 : 1,
        whiteSpace: 'nowrap', transition: 'all 80ms ease',
        ...styles[variant], ...style,
      }}>
      {icon && <Icon name={icon} size={sz.ic} />}
      {children}
    </button>
  );
}

function Input({ value, onChange, placeholder, icon, suffix, style = {}, type = 'text', mono = false }) {
  return (
    <div style={{
      display: 'flex', alignItems: 'center', height: 34,
      background: T.panel, border: `1px solid ${T.border}`,
      borderRadius: 7, padding: '0 10px', gap: 8,
      ...style,
    }}>
      {icon && <Icon name={icon} size={14} color={T.textMute} />}
      <input
        type={type}
        value={value} onChange={onChange} placeholder={placeholder}
        style={{
          flex: 1, background: 'transparent', border: 'none', outline: 'none',
          color: T.text, fontSize: 13, fontFamily: mono ? T.mono : T.font,
          padding: 0, minWidth: 0,
        }}
      />
      {suffix && <span style={{ color: T.textMute, fontSize: 12, fontFamily: T.mono }}>{suffix}</span>}
    </div>
  );
}

function Select({ value, onChange, options, style = {} }) {
  return (
    <div style={{ position: 'relative', ...style }}>
      <select value={value} onChange={onChange}
        style={{
          height: 34, width: '100%',
          background: T.panel, border: `1px solid ${T.border}`,
          borderRadius: 7, padding: '0 32px 0 12px',
          color: T.text, fontSize: 13, fontFamily: T.font,
          appearance: 'none', cursor: 'pointer', outline: 'none',
        }}>
        {options.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
      </select>
      <div style={{ position: 'absolute', right: 10, top: 10, pointerEvents: 'none' }}>
        <Icon name="chevron-down" size={14} color={T.textMute} />
      </div>
    </div>
  );
}

function Card({ children, style = {}, padding = 18 }) {
  return (
    <div style={{
      background: T.panel,
      border: `1px solid ${T.border}`,
      borderRadius: 10,
      padding,
      ...style,
    }}>
      {children}
    </div>
  );
}

function Field({ label, hint, children, span = 1 }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 6, gridColumn: `span ${span}` }}>
      <label style={{ fontSize: 11, fontWeight: 600, color: T.textDim, letterSpacing: '0.02em' }}>
        {label}
        {hint && <span style={{ color: T.textMute, fontWeight: 400, marginLeft: 6, fontFamily: T.mono }}>{hint}</span>}
      </label>
      {children}
    </div>
  );
}

function Tag({ children, color = T.textDim, bg }) {
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: 4,
      padding: '2px 7px', fontSize: 10.5, fontWeight: 600,
      borderRadius: 4, color,
      background: bg || (color + '18'),
      border: `1px solid ${color}26`,
      fontFamily: T.font, letterSpacing: '0.02em',
    }}>{children}</span>
  );
}

function SegmentedControl({ value, onChange, options }) {
  return (
    <div style={{
      display: 'inline-flex', background: T.panel2, borderRadius: 7,
      padding: 3, border: `1px solid ${T.border}`,
    }}>
      {options.map(o => (
        <button key={o.value} onClick={() => onChange(o.value)} style={{
          padding: '5px 12px', fontSize: 12, fontWeight: 600,
          border: 'none', cursor: 'pointer',
          background: value === o.value ? T.panel3 : 'transparent',
          color: value === o.value ? T.text : T.textDim,
          borderRadius: 5, fontFamily: T.font,
        }}>{o.label}</button>
      ))}
    </div>
  );
}

function PageHeader({ title, subtitle, actions }) {
  return (
    <div style={{
      display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between',
      gap: 16, padding: '24px 28px 18px', borderBottom: `1px solid ${T.border}`,
    }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
        <h1 style={{
          margin: 0, fontSize: 20, fontWeight: 700, color: T.text,
          letterSpacing: '-0.01em',
        }}>{title}</h1>
        {subtitle && <p style={{ margin: 0, fontSize: 13, color: T.textDim }}>{subtitle}</p>}
      </div>
      {actions && <div style={{ display: 'flex', gap: 8 }}>{actions}</div>}
    </div>
  );
}

Object.assign(window, {
  Button, Input, Select, Card, Field, Tag, SegmentedControl, PageHeader,
});
