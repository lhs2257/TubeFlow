// Tab 3: 업로드 예약 — Video upload & schedule

const SCHEDULED = [
  { id: 1, title: '문어가 오른발잡이라고? — 동물의 비대칭 뇌 [BIO #14]',     when: '2026-04-28 19:00', status: 'queued',    thumb: '#3A2C26' },
  { id: 2, title: '면접관이 아빠였다 — 실화 사연 모음집 EP.7',                  when: '2026-04-29 20:30', status: 'queued',    thumb: '#26303A' },
  { id: 3, title: '20년 단골 할아버지의 마지막 자리 [감동 실화]',                when: '2026-04-30 18:00', status: 'draft',     thumb: '#3A2632' },
  { id: 4, title: '비행기 창문이 둥근 진짜 이유 (1954년의 그 사고)',             when: '2026-05-01 19:00', status: 'queued',    thumb: '#262E3A' },
  { id: 5, title: '쇼츠: 문어 다리 잘리면 어떻게 될까?',                       when: '2026-04-28 12:00', status: 'published', thumb: '#2D3A26' },
];

const STATUS = {
  queued:    { label: '예약됨',   color: T.amber },
  draft:     { label: '초안',    color: T.textDim },
  published: { label: '게시됨',  color: T.green  },
};

function UploadTab() {
  const [tags, setTags] = useState(['문어', '동물지식', 'TIL', '해양생물', '뇌과학']);
  const [date, setDate] = useState('2026-04-28');
  const [time, setTime] = useState('19:00');
  const [visibility, setVisibility] = useState('public');

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <PageHeader
        title="업로드 예약"
        subtitle="영상을 업로드하고 게시 일정을 관리합니다"
        actions={
          <>
            <Button variant="ghost"     icon="calendar" size="md">캘린더 뷰</Button>
            <Button variant="primary"   icon="upload"   size="md">새 업로드</Button>
          </>
        }
      />

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 380px', flex: 1, minHeight: 0 }}>
        {/* Form */}
        <div style={{ padding: '24px 28px', overflow: 'auto', display: 'flex', flexDirection: 'column', gap: 20 }}>
          {/* Video drop */}
          <div>
            <div style={{ fontSize: 11, fontWeight: 600, color: T.textDim, marginBottom: 8 }}>영상 파일</div>
            <div style={{
              border: `1.5px dashed ${T.borderHi}`,
              borderRadius: 10, padding: 18,
              background: T.panel, display: 'flex', alignItems: 'center', gap: 16,
            }}>
              <div style={{
                width: 96, height: 54,
                background: `linear-gradient(135deg, #3A2632, #2A1A22)`,
                borderRadius: 6, display: 'flex', alignItems: 'center', justifyContent: 'center',
                position: 'relative', flexShrink: 0,
                backgroundImage: 'repeating-linear-gradient(45deg, rgba(255,255,255,0.03) 0 6px, transparent 6px 12px)',
              }}>
                <Icon name="video" size={20} color={T.textDim} />
                <span style={{
                  position: 'absolute', bottom: 4, right: 4,
                  fontSize: 9, fontFamily: T.mono, color: T.text,
                  background: 'rgba(0,0,0,0.65)', padding: '1px 4px', borderRadius: 2,
                }}>4:52</span>
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: 13, fontWeight: 600, color: T.text }}>octopus_handedness_final.mp4</div>
                <div style={{ display: 'flex', gap: 12, fontSize: 11, color: T.textMute, fontFamily: T.mono, marginTop: 4 }}>
                  <span>1920×1080 · 60fps</span>
                  <span>284 MB</span>
                  <span>H.264</span>
                </div>
              </div>
              <Button variant="ghost" size="sm" icon="folder">변경</Button>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: 14 }}>
            <Field label="제목" hint="최대 100자">
              <Input value="문어가 오른발잡이라고? — 동물의 비대칭 뇌 [BIO #14]" onChange={() => {}} suffix="48 / 100" />
            </Field>

            <Field label="설명">
              <textarea
                rows={5}
                defaultValue={`최근 미네소타 대학 해양생물학팀이 발견한 충격적인 사실 —\n문어의 90%는 "세 번째 오른쪽 다리"를 우선적으로 사용합니다.\n\n00:00 인트로\n00:25 핵심 연구 결과\n01:40 왜 세 번째 다리인가?\n...`}
                style={{
                  background: T.panel, border: `1px solid ${T.border}`,
                  borderRadius: 7, padding: '10px 12px', resize: 'none',
                  color: T.text, fontSize: 13, fontFamily: T.font,
                  outline: 'none', lineHeight: 1.55,
                }}
              />
            </Field>

            <Field label="태그" hint={`${tags.length} / 15`}>
              <div style={{
                display: 'flex', flexWrap: 'wrap', gap: 6,
                background: T.panel, border: `1px solid ${T.border}`,
                borderRadius: 7, padding: 8, minHeight: 38,
              }}>
                {tags.map((t, i) => (
                  <span key={i} style={{
                    display: 'inline-flex', alignItems: 'center', gap: 5,
                    padding: '3px 6px 3px 8px', fontSize: 11.5, fontWeight: 500,
                    background: T.panel3, color: T.text,
                    borderRadius: 4, fontFamily: T.font,
                  }}>
                    #{t}
                    <button onClick={() => setTags(tags.filter((_, j) => j !== i))} style={{
                      background: 'none', border: 'none', cursor: 'pointer',
                      color: T.textMute, padding: 0, fontSize: 11,
                    }}>×</button>
                  </span>
                ))}
                <input placeholder="태그 추가..." style={{
                  background: 'transparent', border: 'none', outline: 'none',
                  color: T.text, fontSize: 12, fontFamily: T.font, flex: 1, minWidth: 80,
                }} />
              </div>
            </Field>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14 }}>
            <Field label="썸네일">
              <div style={{
                aspectRatio: '16/9', background: '#3A2632',
                backgroundImage: 'repeating-linear-gradient(45deg, rgba(255,255,255,0.04) 0 8px, transparent 8px 16px)',
                border: `1px solid ${T.border}`, borderRadius: 7,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                color: T.textMute, fontSize: 11, fontFamily: T.mono,
                cursor: 'pointer', position: 'relative',
              }}>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6 }}>
                  <Icon name="image" size={20} color={T.textDim} />
                  thumbnail_v2.jpg
                </div>
              </div>
            </Field>

            <Field label="공개 범위">
              <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                {[
                  { v: 'public',   l: '공개',     d: '모든 사용자' },
                  { v: 'unlisted', l: '미등록',   d: 'URL 보유자만' },
                  { v: 'private',  l: '비공개',   d: '나만 보기'   },
                ].map(o => (
                  <button key={o.v} onClick={() => setVisibility(o.v)} style={{
                    padding: '8px 10px', textAlign: 'left',
                    background: visibility === o.v ? T.panel3 : T.panel,
                    border: `1px solid ${visibility === o.v ? T.accent : T.border}`,
                    borderRadius: 6, cursor: 'pointer',
                    display: 'flex', alignItems: 'center', gap: 8,
                  }}>
                    <div style={{
                      width: 12, height: 12, borderRadius: '50%',
                      border: `2px solid ${visibility === o.v ? T.accent : T.borderHi}`,
                      background: visibility === o.v ? T.accent : 'transparent',
                    }} />
                    <span style={{ fontSize: 12, fontWeight: 600, color: T.text }}>{o.l}</span>
                    <span style={{ fontSize: 11, color: T.textMute, marginLeft: 'auto' }}>{o.d}</span>
                  </button>
                ))}
              </div>
            </Field>
          </div>

          <Card padding={16} style={{ background: T.panel2 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
              <Icon name="clock" size={14} color={T.accent} />
              <span style={{ fontSize: 13, fontWeight: 600, color: T.text }}>예약 게시</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 10 }}>
              <Field label="날짜">
                <Input type="date" value={date} onChange={e => setDate(e.target.value)} />
              </Field>
              <Field label="시간">
                <Input type="time" value={time} onChange={e => setTime(e.target.value)} />
              </Field>
              <Field label="시간대">
                <Select value="kst" onChange={() => {}} options={[
                  { value: 'kst', label: 'KST (UTC+9)' },
                  { value: 'utc', label: 'UTC' },
                  { value: 'pst', label: 'PST (UTC-8)' },
                ]} />
              </Field>
            </div>
            <div style={{
              marginTop: 10, padding: '8px 10px', background: T.bg,
              borderRadius: 5, fontSize: 11.5, color: T.textDim, fontFamily: T.mono,
              border: `1px solid ${T.border}`,
            }}>
              ⏱ 게시까지 약 14시간 32분 · 화요일 저녁 황금시간대 (CTR 예상 6.8%)
            </div>
          </Card>

          <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end', paddingTop: 4 }}>
            <Button variant="ghost"     icon="trash">삭제</Button>
            <Button variant="secondary">초안 저장</Button>
            <Button variant="primary"   icon="upload">예약 등록</Button>
          </div>
        </div>

        {/* Schedule list */}
        <div style={{ borderLeft: `1px solid ${T.border}`, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
          <div style={{
            padding: '14px 20px', borderBottom: `1px solid ${T.border}`,
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          }}>
            <span style={{ fontSize: 13, fontWeight: 600, color: T.text }}>예약 큐</span>
            <Tag color={T.amber}>{SCHEDULED.filter(s => s.status === 'queued').length}개 대기</Tag>
          </div>
          <div style={{ flex: 1, overflow: 'auto', padding: 12, display: 'flex', flexDirection: 'column', gap: 8 }}>
            {SCHEDULED.map(s => (
              <ScheduleCard key={s.id} s={s} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function ScheduleCard({ s }) {
  const st = STATUS[s.status];
  const [hover, setHover] = useState(false);
  return (
    <div
      onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
      style={{
        background: hover ? T.panel2 : T.panel,
        border: `1px solid ${hover ? T.borderHi : T.border}`,
        borderRadius: 8, padding: 10, display: 'flex', gap: 10,
        cursor: 'pointer', transition: 'all 80ms ease',
      }}>
      <div style={{
        width: 80, height: 45, flexShrink: 0,
        background: s.thumb,
        backgroundImage: 'repeating-linear-gradient(45deg, rgba(255,255,255,0.04) 0 6px, transparent 6px 12px)',
        borderRadius: 5,
      }} />
      <div style={{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column', gap: 4 }}>
        <div style={{
          fontSize: 12, fontWeight: 600, color: T.text, lineHeight: 1.35,
          overflow: 'hidden', textOverflow: 'ellipsis',
          display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical',
        }}>{s.title}</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <Tag color={st.color}>{st.label}</Tag>
          <span style={{ fontSize: 10.5, color: T.textMute, fontFamily: T.mono }}>{s.when}</span>
        </div>
      </div>
    </div>
  );
}

window.UploadTab = UploadTab;
