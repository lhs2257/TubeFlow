// Tab 1: 소재 수집 — Reddit content collector

const SUBREDDITS_PRESET = ['r/AskReddit', 'r/todayilearned', 'r/explainlikeimfive', 'r/MaliciousCompliance'];

const MOCK_POSTS = [
  { sel: true,  title: '20년간 매일 같은 자리에 앉던 할아버지가 사라진 날, 카페 단골들이 한 일',          sub: 'r/MadeMeSmile',      score: '48.2k', cmts: '2.1k', age: '14h', flair: 'Heartwarming' },
  { sel: true,  title: 'TIL 문어는 왼발잡이 오른발잡이가 있고, 90%는 세 번째 오른쪽 다리를 우선 사용한다',  sub: 'r/todayilearned',    score: '31.7k', cmts: '892',  age: '8h',  flair: 'Animals'      },
  { sel: false, title: '회사에서 "어차피 다 인생경험" 한 번 듣고 정확히 9시 5초에 퇴근하기 시작한 결과',     sub: 'r/MaliciousCompliance', score: '24.0k', cmts: '1.4k', age: '1d',  flair: 'M'            },
  { sel: true,  title: '면접 끝나고 5분 뒤에 합격 전화 받았는데, 알고 보니 면접관이 우리 아빠였다',          sub: 'r/AskReddit',        score: '19.6k', cmts: '3.0k', age: '2d',  flair: 'Story'        },
  { sel: false, title: 'ELI5: 왜 비행기 창문은 둥근 모서리로 만들어져 있나요?',                              sub: 'r/explainlikeimfive', score: '14.3k', cmts: '518',  age: '6h',  flair: 'Engineering'  },
  { sel: false, title: '10년 전 산 적금 통장을 정리하다가 발견한 5천만원의 비밀',                            sub: 'r/personalfinance',   score: '12.1k', cmts: '702',  age: '3d',  flair: 'Money'        },
  { sel: false, title: '우리 강아지가 매일 아침 7시에 정확히 짖는 이유를 1년 만에 알아냈다',                  sub: 'r/aww',              score: '9.8k',  cmts: '341',  age: '12h', flair: 'Dogs'         },
  { sel: false, title: '15년 차 셰프가 절대로 집에서 안 만드는 음식 7가지',                                  sub: 'r/AskCulinary',      score: '8.4k',  cmts: '1.1k', age: '2d',  flair: 'Tips'         },
];

function CollectTab() {
  const [subreddits, setSubreddits] = useState('r/AskReddit, r/todayilearned, r/MaliciousCompliance');
  const [period, setPeriod] = useState('week');
  const [sort, setSort] = useState('top');
  const [limit, setLimit] = useState(50);
  const [posts, setPosts] = useState(MOCK_POSTS);
  const [running, setRunning] = useState(false);
  const [progress, setProgress] = useState(0);

  const selectedCount = posts.filter(p => p.sel).length;

  function runCollect() {
    setRunning(true); setProgress(0);
    const id = setInterval(() => {
      setProgress(p => {
        if (p >= 100) { clearInterval(id); setRunning(false); return 100; }
        return p + 7;
      });
    }, 90);
  }

  function toggle(i) {
    setPosts(prev => prev.map((p, idx) => idx === i ? { ...p, sel: !p.sel } : p));
  }
  function toggleAll() {
    const all = posts.every(p => p.sel);
    setPosts(prev => prev.map(p => ({ ...p, sel: !all })));
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <PageHeader
        title="소재 수집"
        subtitle="Reddit, Hacker News 등에서 콘텐츠 소재를 자동으로 수집합니다"
        actions={
          <>
            <Button variant="secondary" icon="folder" size="md">최근 수집</Button>
            <Button variant="secondary" icon="settings" size="md">소스 관리</Button>
          </>
        }
      />

      <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', flex: 1, minHeight: 0 }}>
        {/* Left: collection settings */}
        <div style={{ padding: '20px 24px', borderRight: `1px solid ${T.border}`, overflow: 'auto', display: 'flex', flexDirection: 'column', gap: 16 }}>
          <Field label="서브레딧" hint="쉼표로 구분">
            <textarea
              value={subreddits}
              onChange={e => setSubreddits(e.target.value)}
              rows={3}
              style={{
                background: T.panel, border: `1px solid ${T.border}`,
                borderRadius: 7, padding: '8px 10px', resize: 'none',
                color: T.text, fontSize: 12.5, fontFamily: T.mono,
                outline: 'none', lineHeight: 1.5,
              }}
            />
          </Field>

          <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
            {SUBREDDITS_PRESET.map(s => (
              <button key={s} onClick={() => {
                if (!subreddits.includes(s)) setSubreddits(p => p ? `${p}, ${s}` : s);
              }} style={{
                padding: '4px 8px', fontSize: 11, fontFamily: T.mono,
                background: T.panel2, color: T.textDim,
                border: `1px solid ${T.border}`, borderRadius: 5,
                cursor: 'pointer',
              }}>+ {s}</button>
            ))}
          </div>

          <div style={{ height: 1, background: T.border, margin: '4px 0' }} />

          <Field label="기간">
            <SegmentedControl
              value={period} onChange={setPeriod}
              options={[
                { value: 'day',   label: '24h'  },
                { value: 'week',  label: '1주' },
                { value: 'month', label: '1달' },
                { value: 'year',  label: '1년' },
              ]}
            />
          </Field>

          <Field label="정렬">
            <Select value={sort} onChange={e => setSort(e.target.value)}
              options={[
                { value: 'top',  label: '추천순 (Top)' },
                { value: 'hot',  label: '인기순 (Hot)' },
                { value: 'new',  label: '최신순 (New)' },
                { value: 'rising', label: '떠오르는 (Rising)' },
              ]}
            />
          </Field>

          <Field label="개수" hint={`${limit}개`}>
            <input type="range" min="10" max="200" step="10" value={limit}
              onChange={e => setLimit(+e.target.value)}
              style={{ width: '100%', accentColor: T.accent }}
            />
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 10, color: T.textMute, fontFamily: T.mono }}>
              <span>10</span><span>100</span><span>200</span>
            </div>
          </Field>

          <Field label="최소 추천수" hint="0 = 제한 없음">
            <Input value="500" mono suffix="upvotes" onChange={() => {}} />
          </Field>

          <div style={{ flex: 1 }} />

          <Button variant="primary" icon="spark" size="lg" onClick={runCollect} disabled={running}>
            {running ? `수집 중 ${progress}%` : '수집 실행'}
          </Button>

          {running && (
            <div style={{ height: 3, background: T.panel3, borderRadius: 2, overflow: 'hidden' }}>
              <div style={{ height: '100%', width: `${progress}%`, background: T.accent, transition: 'width 80ms linear' }} />
            </div>
          )}
        </div>

        {/* Right: results table */}
        <div style={{ display: 'flex', flexDirection: 'column', minWidth: 0 }}>
          <div style={{
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            padding: '14px 24px', borderBottom: `1px solid ${T.border}`,
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <span style={{ fontSize: 13, fontWeight: 600, color: T.text }}>수집된 소재</span>
              <Tag color={T.textDim}>{posts.length}개</Tag>
              {selectedCount > 0 && <Tag color={T.accent}>{selectedCount}개 선택됨</Tag>}
            </div>
            <div style={{ display: 'flex', gap: 8 }}>
              <Button variant="ghost" size="sm" icon="check" onClick={toggleAll}>전체 선택</Button>
              <Button variant="secondary" size="sm" icon="folder" disabled={selectedCount === 0}>저장</Button>
              <Button variant="primary" size="sm" icon="script" disabled={selectedCount === 0}>대본으로 보내기</Button>
            </div>
          </div>

          <div style={{ flex: 1, overflow: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12.5 }}>
              <thead style={{
                position: 'sticky', top: 0, background: T.bg,
                borderBottom: `1px solid ${T.border}`, zIndex: 1,
              }}>
                <tr style={{ color: T.textMute }}>
                  <th style={th(40)}></th>
                  <th style={th(0, true)}>제목</th>
                  <th style={th(120)}>출처</th>
                  <th style={th(80)}>추천</th>
                  <th style={th(70)}>댓글</th>
                  <th style={th(70)}>경과</th>
                  <th style={th(40)}></th>
                </tr>
              </thead>
              <tbody>
                {posts.map((p, i) => (
                  <PostRow key={i} post={p} onToggle={() => toggle(i)} />
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

function th(width, left) {
  return {
    padding: '10px 12px',
    textAlign: left ? 'left' : 'right',
    fontSize: 10.5, fontWeight: 600, letterSpacing: '0.06em',
    width: width || 'auto',
  };
}

function PostRow({ post, onToggle }) {
  const [hover, setHover] = useState(false);
  return (
    <tr
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        borderBottom: `1px solid ${T.border}`,
        background: hover ? T.panel : 'transparent',
        cursor: 'pointer',
      }}
      onClick={onToggle}>
      <td style={{ padding: '12px', textAlign: 'center' }}>
        <Checkbox checked={post.sel} />
      </td>
      <td style={{ padding: '12px', color: T.text, lineHeight: 1.45 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Icon name="reddit" size={13} color="#FF7A45" />
          <span style={{ fontWeight: 500 }}>{post.title}</span>
        </div>
        <div style={{ marginTop: 4, display: 'flex', gap: 6 }}>
          <Tag color={T.textMute}>{post.flair}</Tag>
        </div>
      </td>
      <td style={{ padding: '12px', textAlign: 'right', color: T.textDim, fontFamily: T.mono, fontSize: 11.5 }}>{post.sub}</td>
      <td style={{ padding: '12px', textAlign: 'right', color: T.text, fontFamily: T.mono, fontSize: 12 }}>
        <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
          <Icon name="arrow-up" size={11} color={T.green} />{post.score}
        </span>
      </td>
      <td style={{ padding: '12px', textAlign: 'right', color: T.textDim, fontFamily: T.mono, fontSize: 12 }}>{post.cmts}</td>
      <td style={{ padding: '12px', textAlign: 'right', color: T.textMute, fontFamily: T.mono, fontSize: 11.5 }}>{post.age}</td>
      <td style={{ padding: '12px', textAlign: 'center' }}>
        <Icon name="eye" size={14} color={T.textMute} />
      </td>
    </tr>
  );
}

function Checkbox({ checked }) {
  return (
    <div style={{
      width: 16, height: 16, borderRadius: 4,
      background: checked ? T.accent : 'transparent',
      border: `1.5px solid ${checked ? T.accent : T.borderHi}`,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      transition: 'all 80ms ease',
    }}>
      {checked && <Icon name="check" size={10} color="#fff" />}
    </div>
  );
}

window.CollectTab = CollectTab;
