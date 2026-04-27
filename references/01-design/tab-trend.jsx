// Tab 4: 트렌드 분석 — YouTube/Google Trends report

const KEYWORDS = ['문어', '심해 생물', '동물 지능', 'TIL'];

const TRENDS_TOP = [
  { rank: 1,  kw: '심해 생물 다큐',    delta: '+184%', vol: '92k',  region: 'KR', heat: 0.95 },
  { rank: 2,  kw: '문어 지능',         delta: '+76%',  vol: '54k',  region: 'KR', heat: 0.78 },
  { rank: 3,  kw: '바다 미스터리',      delta: '+62%',  vol: '48k',  region: 'KR', heat: 0.71 },
  { rank: 4,  kw: 'TIL 동물',          delta: '+41%',  vol: '32k',  region: 'KR', heat: 0.58 },
  { rank: 5,  kw: '해양 다큐멘터리',     delta: '+28%',  vol: '27k',  region: 'KR', heat: 0.50 },
  { rank: 6,  kw: '신기한 사실',         delta: '+19%',  vol: '24k',  region: 'KR', heat: 0.44 },
  { rank: 7,  kw: '뇌과학',             delta: '+14%',  vol: '21k',  region: 'KR', heat: 0.38 },
  { rank: 8,  kw: '동물 행동학',         delta: '+8%',   vol: '18k',  region: 'KR', heat: 0.32 },
  { rank: 9,  kw: '문어 요리',           delta: '−4%',   vol: '15k',  region: 'KR', heat: 0.25, down: true },
  { rank: 10, kw: '수족관 영상',         delta: '−12%',  vol: '11k',  region: 'KR', heat: 0.18, down: true },
];

// Smooth synthetic series
const SERIES = [
  { name: '문어',         color: T.accent, data: [22, 25, 28, 31, 33, 38, 42, 48, 51, 56, 64, 71, 80, 86, 92, 95] },
  { name: '심해 생물',    color: T.blue,   data: [40, 42, 44, 46, 49, 53, 58, 62, 66, 70, 74, 78, 82, 85, 88, 90] },
  { name: '동물 지능',    color: T.green,  data: [55, 56, 58, 60, 61, 60, 58, 55, 53, 52, 54, 57, 60, 64, 67, 69] },
  { name: 'TIL',          color: T.amber,  data: [30, 31, 32, 33, 34, 35, 36, 36, 37, 37, 38, 38, 39, 40, 41, 42] },
];

function TrendTab() {
  const [range, setRange] = useState('30d');
  const [region, setRegion] = useState('kr');
  const [keywords, setKeywords] = useState(KEYWORDS);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <PageHeader
        title="트렌드 분석"
        subtitle="YouTube · Google Trends 데이터로 콘텐츠 기회를 발굴합니다"
        actions={
          <>
            <Button variant="ghost"     icon="folder" size="md">저장된 리포트</Button>
            <Button variant="primary"   icon="check"  size="md">리포트 저장</Button>
          </>
        }
      />

      {/* Controls bar */}
      <div style={{
        display: 'flex', alignItems: 'center', gap: 14,
        padding: '14px 28px', borderBottom: `1px solid ${T.border}`,
        flexWrap: 'wrap',
      }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, flex: 1, minWidth: 280 }}>
          {keywords.map((k, i) => (
            <span key={i} style={{
              display: 'inline-flex', alignItems: 'center', gap: 6,
              padding: '5px 8px 5px 10px', fontSize: 12, fontWeight: 600,
              background: T.panel2, color: T.text,
              borderRadius: 6, border: `1px solid ${T.border}`,
            }}>
              <span style={{ width: 6, height: 6, borderRadius: '50%', background: SERIES[i % SERIES.length].color }} />
              {k}
              <button onClick={() => setKeywords(keywords.filter((_, j) => j !== i))} style={{
                background: 'none', border: 'none', cursor: 'pointer',
                color: T.textMute, fontSize: 13, padding: 0, marginLeft: 2,
              }}>×</button>
            </span>
          ))}
          <button style={{
            display: 'inline-flex', alignItems: 'center', gap: 4,
            padding: '5px 10px', fontSize: 12, fontWeight: 500,
            background: 'transparent', color: T.textDim,
            border: `1px dashed ${T.borderHi}`, borderRadius: 6,
            cursor: 'pointer', fontFamily: T.font,
          }}>
            <Icon name="plus" size={11} /> 키워드 추가
          </button>
        </div>
        <SegmentedControl value={range} onChange={setRange} options={[
          { value: '7d',  label: '7일' },
          { value: '30d', label: '30일' },
          { value: '90d', label: '90일' },
          { value: '1y',  label: '1년' },
        ]} />
        <Select value={region} onChange={e => setRegion(e.target.value)}
          style={{ width: 140 }}
          options={[
            { value: 'kr', label: '🇰🇷 한국' },
            { value: 'us', label: '🇺🇸 미국' },
            { value: 'jp', label: '🇯🇵 일본' },
            { value: 'global', label: '🌐 글로벌' },
          ]}
        />
      </div>

      <div style={{ flex: 1, overflow: 'auto', padding: 28, display: 'flex', flexDirection: 'column', gap: 20 }}>
        {/* Stat row */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12 }}>
          <Stat label="총 검색량" value="1.24M" delta="+34%" up icon="globe" />
          <Stat label="평균 경쟁도" value="중" valueColor={T.amber} delta="−8%" icon="trend" />
          <Stat label="최고 키워드" value="심해 생물" delta="+184%" up icon="spark" />
          <Stat label="추천 게시 시간" value="화 19:00" delta="CTR 6.8%" icon="clock" />
        </div>

        {/* Chart */}
        <Card padding={20}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 14 }}>
            <div>
              <div style={{ fontSize: 13, fontWeight: 600, color: T.text }}>관심도 추이</div>
              <div style={{ fontSize: 11, color: T.textMute, marginTop: 2, fontFamily: T.mono }}>
                Google Trends · 최근 {range} · 정규화 0–100
              </div>
            </div>
            <div style={{ display: 'flex', gap: 14 }}>
              {SERIES.map(s => (
                <div key={s.name} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 11.5, color: T.textDim }}>
                  <span style={{ width: 8, height: 2, background: s.color, borderRadius: 1 }} />
                  {s.name}
                </div>
              ))}
            </div>
          </div>
          <Chart series={SERIES} />
        </Card>

        {/* Top keywords table */}
        <Card padding={0}>
          <div style={{
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            padding: '14px 20px', borderBottom: `1px solid ${T.border}`,
          }}>
            <div style={{ fontSize: 13, fontWeight: 600, color: T.text }}>인기 키워드 순위</div>
            <Button variant="ghost" size="sm" icon="folder">CSV 내보내기</Button>
          </div>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12.5 }}>
            <thead>
              <tr style={{ color: T.textMute }}>
                <th style={{ ...th(50, true), paddingLeft: 20 }}>#</th>
                <th style={th(0, true)}>키워드</th>
                <th style={th(120)}>변화율</th>
                <th style={th(100)}>검색량</th>
                <th style={th(80)}>지역</th>
                <th style={{ ...th(180), paddingRight: 20 }}>관심도</th>
              </tr>
            </thead>
            <tbody>
              {TRENDS_TOP.map(t => (
                <tr key={t.rank} style={{ borderTop: `1px solid ${T.border}` }}>
                  <td style={{ padding: '10px 20px', color: T.textMute, fontFamily: T.mono, fontSize: 12 }}>{t.rank.toString().padStart(2, '0')}</td>
                  <td style={{ padding: '10px 12px', color: T.text, fontWeight: 500 }}>{t.kw}</td>
                  <td style={{ padding: '10px 12px', textAlign: 'right' }}>
                    <span style={{
                      display: 'inline-flex', alignItems: 'center', gap: 4,
                      color: t.down ? T.accent : T.green, fontFamily: T.mono, fontWeight: 600,
                    }}>
                      <Icon name={t.down ? 'arrow-down' : 'arrow-up'} size={11} />
                      {t.delta.replace('+','').replace('−','')}
                    </span>
                  </td>
                  <td style={{ padding: '10px 12px', textAlign: 'right', color: T.textDim, fontFamily: T.mono }}>{t.vol}</td>
                  <td style={{ padding: '10px 12px', textAlign: 'right', color: T.textMute, fontFamily: T.mono, fontSize: 11 }}>{t.region}</td>
                  <td style={{ padding: '10px 20px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <div style={{ flex: 1, height: 4, background: T.panel3, borderRadius: 2, overflow: 'hidden' }}>
                        <div style={{ width: `${t.heat * 100}%`, height: '100%', background: t.down ? T.textDim : T.accent }} />
                      </div>
                      <span style={{ fontSize: 11, color: T.textDim, fontFamily: T.mono, width: 30, textAlign: 'right' }}>
                        {Math.round(t.heat * 100)}
                      </span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      </div>
    </div>
  );
}

function Stat({ label, value, delta, up, valueColor, icon }) {
  return (
    <Card padding={14}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 10 }}>
        <span style={{ fontSize: 11, fontWeight: 600, color: T.textMute, letterSpacing: '0.04em' }}>{label}</span>
        <Icon name={icon} size={14} color={T.textMute} />
      </div>
      <div style={{ fontSize: 22, fontWeight: 700, color: valueColor || T.text, letterSpacing: '-0.01em', lineHeight: 1.1 }}>{value}</div>
      <div style={{
        marginTop: 6, fontSize: 11, fontFamily: T.mono,
        color: up ? T.green : T.textDim,
      }}>{delta}</div>
    </Card>
  );
}

function Chart({ series }) {
  const W = 800, H = 220, P = { l: 36, r: 12, t: 10, b: 24 };
  const innerW = W - P.l - P.r, innerH = H - P.t - P.b;
  const len = series[0].data.length;
  const xAt = i => P.l + (innerW * i) / (len - 1);
  const yAt = v => P.t + innerH - (innerH * v) / 100;

  function path(data) {
    return data.map((v, i) => {
      const x = xAt(i), y = yAt(v);
      if (i === 0) return `M ${x} ${y}`;
      const px = xAt(i - 1), py = yAt(data[i - 1]);
      const cx1 = px + (x - px) / 2, cx2 = px + (x - px) / 2;
      return `C ${cx1} ${py} ${cx2} ${y} ${x} ${y}`;
    }).join(' ');
  }
  function area(data) {
    return path(data) + ` L ${xAt(len - 1)} ${P.t + innerH} L ${P.l} ${P.t + innerH} Z`;
  }

  return (
    <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', height: 240, display: 'block' }}>
      <defs>
        {series.map((s, i) => (
          <linearGradient key={i} id={`g-${i}`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%"   stopColor={s.color} stopOpacity="0.18" />
            <stop offset="100%" stopColor={s.color} stopOpacity="0" />
          </linearGradient>
        ))}
      </defs>
      {/* gridlines */}
      {[0, 25, 50, 75, 100].map(v => (
        <g key={v}>
          <line x1={P.l} x2={W - P.r} y1={yAt(v)} y2={yAt(v)} stroke={T.border} strokeWidth="1" />
          <text x={P.l - 6} y={yAt(v) + 3} fill={T.textMute} fontSize="9.5" fontFamily={T.mono} textAnchor="end">{v}</text>
        </g>
      ))}
      {/* x labels */}
      {[0, 4, 8, 12, 15].map(i => (
        <text key={i} x={xAt(i)} y={H - 6} fill={T.textMute} fontSize="9.5" fontFamily={T.mono} textAnchor="middle">
          {`D-${15 - i}`}
        </text>
      ))}
      {/* areas */}
      {series.map((s, i) => i === 0 && (
        <path key={i} d={area(s.data)} fill={`url(#g-${i})`} />
      ))}
      {/* lines */}
      {series.map((s, i) => (
        <path key={i} d={path(s.data)} fill="none" stroke={s.color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      ))}
      {/* end dots */}
      {series.map((s, i) => (
        <circle key={i} cx={xAt(len - 1)} cy={yAt(s.data[len - 1])} r="3.5" fill={s.color} stroke={T.bg} strokeWidth="2" />
      ))}
    </svg>
  );
}

window.TrendTab = TrendTab;
