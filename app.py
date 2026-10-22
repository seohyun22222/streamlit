import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="거대한 뿔의 역설: 3D 핸디캡 원리 시뮬레이터",
    page_icon="🦌",
    layout="wide",
)

# 메인 타이틀
st.title("🦌 거대한 뿔의 역설: 3D 핸디캡 원리 시뮬레이터")
st.caption(
    "진화생물학 탐구 대시보드 | 자연선택, 핸디캡 원리, 그리고 진화적으로 안정된 전략(ESS)"
)

# 상단 탭 구성 (탐구 동기, 3D 시뮬레이션, 수리적 원리, 결과 분석)
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "💡 1. 탐구 동기",
        "🧪 2. 3D 리얼 시뮬레이션",
        "📐 3. 작동 원리 및 모델링",
        "📊 4. 결과 분석 및 고찰",
    ]
)

# ==========================================
# 1. 탐구 동기 탭
# ==========================================
with tab1:
    st.header("💡 탐구 동기 및 핵심 요약")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
        ### 1. 자연선택: 완벽함이 아닌 '차선의 최적화'
        - 자연선택은 모든 생물을 완벽하게 진화시키는 전지전능한 설계도가 아닙니다.
        - 주어진 환경과 유전적 제약 안에서 다음 세대에 유전자를 더 많이 남기기 위해 작동하는 **엄혹한 상대적 필터링 메커니즘**입니다.
        
        ### 2. 핸디캡 원리: '손해'를 통한 신뢰의 증명
        - 사슴의 거대한 뿔처럼 생존에 방해가 되는 과시적 낭비는 가짜가 감히 흉내 낼 수 없는 극단적인 비용을 치름으로써, **자신의 유전적 우수성을 증명하는 방법**이 됩니다.
        """)

    with col2:
        st.markdown("""
        ### 3. 진화적으로 안정된 전략 (ESS): 비용과 이득의 수학적 균형
        - 뿔이 너무 작으면 싸움 비용이 늘어나고, 너무 크면 유지 에너지가 고갈됩니다.
        - 자연선택은 이 두 비용 사이에서 생존 효율을 극대화하는 **최적의 타협점**을 찾아내며, 이것이 바로 진화가 만들어낸 정교한 균형 감각입니다.
        """)
        st.info(
            "👉 상단 **'🧪 2. 3D 리얼 시뮬레이션'** 탭으로 이동하여 뿔 크기에 따른 사슴의 실제 움직임과 생존 변화를 관찰해 보세요!"
        )

# ==========================================
# 2. 3D 리얼 시뮬레이션 탭
# ==========================================
with tab2:
    st.header("🧪 3D 사슴 생태 시뮬레이션")
    st.markdown(
        "사이드바에서 **'뿔 크기'**를 조절하면 3D 캔버스에 사슴의 뿔 모양이 즉시 반영되고, 라이벌과 만났을 때의 행동 패턴이 계산됩니다."
    )

    # 사이드바 입력 설정
    st.sidebar.header("⚙️ 시뮬레이션 환경 변수")
    antler_size = st.sidebar.slider(
        "뿔 크기 (Handicap Level)",
        min_value=0,
        max_value=100,
        value=50,
        step=5,
        help="0: 아주 작음 | 50: 적정 크기 | 100: 극단적으로 큼",
    )
    stamina_input = st.sidebar.slider("기초 체력 (HP)", 50, 300, 150, 10)
    rounds_input = st.sidebar.slider("영역 다툼 횟수 (Rounds)", 5, 30, 15, 5)

    # VPython (GlowScript 3D) HTML 생성 함수
    def generate_vpython_3d_deer(antler_val):
        # 뿔 크기 스케일링
        antler_scale = 0.2 + (antler_val / 100.0) * 1.5

        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <script type="text/javascript" src="https://www.glowscript.org/lib/jquery/2.1.0/jquery.min.js"></script>
            <script type="text/javascript" src="https://www.glowscript.org/lib/jquery/1.10.4/jquery-ui.custom.min.js"></script>
            <script type="text/javascript" src="https://www.glowscript.org/package/glow.3.2.min.js"></script>
            <script type="text/javascript" src="https://www.glowscript.org/package/RSrun.3.2.min.js"></script>
        </head>
        <body style="margin:0; padding:0; overflow:hidden;">
            <div id="glowscript" class="glowscript"></div>
            <script type="text/javascript">
                async function __main__() {{
                    var version = ["3.2", "glowscript"];
                    window.__context = {{ glowscript_container: $("#glowscript") }};
                    
                    var scene = canvas({{
                        width: 700, 
                        height: 420, 
                        background: vec(0.12, 0.15, 0.18),
                        center: vec(0, 1, 0),
                        forward: vec(-1, -0.4, -1)
                    }});
                    
                    // 들판 바닥
                    var ground = box({{pos: vec(0,-0.1,0), size: vec(15, 0.2, 15), color: vec(0.2, 0.45, 0.2)}});
                    
                    // 3D 사슴 모델링 그룹
                    var body = cylinder({{pos: vec(-1, 1.2, 0), axis: vec(2, 0, 0), radius: 0.5, color: vec(0.6, 0.35, 0.15)}});
                    var neck = cylinder({{pos: vec(0.8, 1.2, 0), axis: vec(0.4, 0.8, 0), radius: 0.25, color: vec(0.6, 0.35, 0.15)}});
                    var head = sphere({{pos: vec(1.2, 2.1, 0), radius: 0.35, color: vec(0.55, 0.3, 0.12)}});
                    
                    // 다리 4개
                    var leg1 = cylinder({{pos: vec(-0.8, 1.2, 0.3), axis: vec(0, -1.2, 0), radius: 0.1, color: vec(0.5, 0.28, 0.1)}});
                    var leg2 = cylinder({{pos: vec(-0.8, 1.2, -0.3), axis: vec(0, -1.2, 0), radius: 0.1, color: vec(0.5, 0.28, 0.1)}});
                    var leg3 = cylinder({{pos: vec(0.6, 1.2, 0.3), axis: vec(0, -1.2, 0), radius: 0.1, color: vec(0.5, 0.28, 0.1)}});
                    var leg4 = cylinder({{pos: vec(0.6, 1.2, -0.3), axis: vec(0, -1.2, 0), radius: 0.1, color: vec(0.5, 0.28, 0.1)}});
                    
                    // 3D 뿔 (Antlers) - 파라미터 적용
                    var scale = {antler_scale};
                    var antler_left_main = cylinder({{pos: vec(1.2, 2.3, 0.15), axis: vec(0.2*scale, 0.9*scale, 0.4*scale), radius: 0.06, color: vec(0.85, 0.75, 0.5)}});
                    var antler_left_branch = cylinder({{pos: vec(1.3, 2.7, 0.3), axis: vec(0.4*scale, 0.3*scale, -0.2*scale), radius: 0.04, color: vec(0.85, 0.75, 0.5)}});
                    
                    var antler_right_main = cylinder({{pos: vec(1.2, 2.3, -0.15), axis: vec(0.2*scale, 0.9*scale, -0.4*scale), radius: 0.06, color: vec(0.85, 0.75, 0.5)}});
                    var antler_right_branch = cylinder({{pos: vec(1.3, 2.7, -0.3), axis: vec(0.4*scale, 0.3*scale, 0.2*scale), radius: 0.04, color: vec(0.85, 0.75, 0.5)}});
                    
                    // 숨쉬기/움직임 애니메이션
                    var t = 0;
                    while (true) {{
                        await rate(30);
                        t += 0.08;
                        head.pos.y = 2.1 + Math.sin(t) * 0.05;
                        antler_left_main.pos.y = 2.3 + Math.sin(t) * 0.05;
                        antler_left_branch.pos.y = 2.7 + Math.sin(t) * 0.05;
                        antler_right_main.pos.y = 2.3 + Math.sin(t) * 0.05;
                        antler_right_branch.pos.y = 2.7 + Math.sin(t) * 0.05;
                    }}
                }}
                $(document).ready(function() {{ __main__(); }});
            </script>
        </body>
        </html>
        """
        return html_code

    # 3D 시뮬레이션 계산 로직
    def run_simulation(antler, stamina, total_rounds):
        energy = float(stamina)
        energy_history = [energy]
        intimidations, defeats = 0, 0

        weight_cost = antler * 0.18
        challenge_prob = max(0.10, 0.90 - (antler / 100.0) * 0.75)

        for r in range(1, total_rounds + 1):
            if energy <= 0:
                break
            energy -= weight_cost

            if np.random.rand() < challenge_prob:
                damage = max(5.0, 40.0 - (antler * 0.35))
                energy -= damage
                defeats += 1
            else:
                intimidations += 1

            energy = max(0.0, energy)
            energy_history.append(energy)

        return energy, energy_history, intimidations, defeats

    col_3d, col_res = st.columns([3, 2])

    with col_3d:
        st.subheader("🖥️ 3D 사슴 개체 렌더링")
        st.caption(
            "마우스 오른쪽 클릭 후 드래그하여 3D 시점을 회전할 수 있습니다."
        )
        html_content = generate_vpython_3d_deer(antler_size)
        components.html(html_content, height=440, scrolling=False)

    with col_res:
        st.subheader("📊 시뮬레이션 실행 결과")
        final_energy, history, intimidations, defeats = run_simulation(
            antler_size, stamina_input, rounds_input
        )

        st.metric(
            "생존 상태",
            "🎉 생존 성공" if final_energy > 0 else "☠️ 사멸 (체력 고갈)",
        )
        st.metric("남은 체력 (HP)", f"{final_energy:.1f} HP")
        st.metric(
            "라이벌 퇴치(위협 성공)",
            f"{intimidations} 회",
            help="뿔을 보고 싸움을 피한 횟수",
        )
        st.metric(
            "직접 충돌(싸움 발생)",
            f"{defeats} 회",
            help="라이벌이 덤벼들어 손상을 입은 횟수",
        )

    # 잔여 체력 그래프
    df_chart = pd.DataFrame(
        {"라운드": list(range(len(history))), "체력(HP)": history}
    )
    fig = px.line(
        df_chart,
        x="라운드",
        y="체력(HP)",
        title=f"뿔 크기 [{antler_size}] 사슴의 체력 변화 추이",
        markers=True,
    )
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 3. 작동 원리 및 모델링 탭
# ==========================================
with tab3:
    st.header("📐 핸디캡 원리의 수리적 모델링")

    st.markdown("""
    이 시뮬레이터는 두 가지 상충하는 비용(Trade-off)의 상호작용을 수학적으로 모델링합니다.
    """)

    col_m1, col_m2 = st.columns(2)

    with col_m1:
        st.subheader("1. 뿔 유지 비용 (Handicap Cost)")
        st.latex(r"\text{Cost}_{weight} = \text{Antler} \times 0.18")
        st.markdown(
            "- 뿔이 무거울수록 이동과 목 지탱에 드는 매 라운드 **기초 체력 소모가 증가**합니다."
        )

    with col_m2:
        st.subheader("2. 라이벌의 도전 확률 (Deterrence Effect)")
        st.latex(
            r"P_{\text{challenge}} = \max\left(0.10, 0.90 - \frac{\text{Antler}}{100} \times 0.75\right)"
        )
        st.markdown(
            "- 뿔이 거대할수록 라이벌이 상대의 강함을 인지하여 **싸움을 포기하고 도망칠 확률이 높아집니다.**"
        )

# ==========================================
# 4. 결과 분석 및 고찰 탭
# ==========================================
with tab4:
    st.header("📊 결과 분석 및 생물학적 고찰")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.error("❌ 뿔 크기 0 ~ 25 (핸디캡 부족)")
        st.markdown("""
        - **원인:** 뿔 유지 비용은 적지만 라이벌에게 강함을 증명하지 못함.
        - **결과:** 라이벌들이 연이어 싸움을 걸어와 **전투 피로와 손상으로 사멸**.
        """)

    with c2:
        st.success("✅ 뿔 크기 35 ~ 65 (최적의 ESS)")
        st.markdown("""
        - **원인:** 무혈입성의 '위협 이득'과 '유지 비용'이 완벽한 균형을 이룸.
        - **결과:** 불필요한 싸움을 회피하고 체력을 보존하여 **자연선택에 의해 우세종으로 생존**.
        """)

    with c3:
        st.warning("⚠️ 뿔 크기 75 ~ 100 (과도한 핸디캡)")
        st.markdown("""
        - **원인:** 라이벌은 완벽히 제압했으나 뿔 자체가 너무 무거움.
        - **결과:** 싸우지도 않고 **스스로 굶어 죽거나 체력이 고갈되어 자멸**.
        """)
