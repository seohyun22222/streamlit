import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="거대한 뿔의 역설: 핸디캡 원리 시뮬레이터",
    page_icon="🦌",
    layout="wide",
)

# 메인 타이틀
st.title("🦌 거대한 뿔의 역설: 핸디캡 원리(Handicap Principle) 시뮬레이터")
st.caption(
    "진화생물학 탐구 대시보드 | 자연선택, 핸디캡 원리, 그리고 진화적으로 안정된 전략(ESS)"
)

# 4가지 메인 탭 구성
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "💡 1. 탐구 동기",
        "🧪 2. 인터랙티브 시뮬레이션",
        "📐 3. 작동 원리 및 수리 모델",
        "📊 4. 결과 분석 및 고찰",
    ]
)

# ==========================================
# 1. 탐구 동기 탭
# ==========================================
with tab1:
    st.header("💡 탐구 동기 및 핵심 요약")

    col1, col2 = st.columns(2)

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
        st.success(
            "👉 상단 **'🧪 2. 인터랙티브 시뮬레이션'** 탭으로 이동하여 뿔 크기에 따른 생존 변화를 직접 실험해 보세요!"
        )

# ==========================================
# 2. 인터랙티브 시뮬레이션 탭
# ==========================================
with tab2:
    st.header("🧪 사슴 생태계 시뮬레이터")
    st.markdown(
        "사이드바에서 변수를 조절한 뒤 시뮬레이션을 실행하여 뿔 크기에 따른 생존 결과를 확인하세요."
    )

    # 사이드바 설정 파라미터
    st.sidebar.header("⚙️ 시뮬레이션 환경 변수")
    antler_size = st.sidebar.slider(
        "내 사슴 뿔 크기 (Handicap Level)",
        min_value=0,
        max_value=100,
        value=50,
        step=5,
        help="0: 아주 작음 | 50: 적정 크기 | 100: 극단적으로 큼",
    )
    stamina_input = st.sidebar.slider("기초 체력 (HP)", 50, 300, 150, 10)
    rounds_input = st.sidebar.slider("영역 다툼 횟수 (Rounds)", 5, 30, 15, 5)

    run_sim = st.button("🚀 시뮬레이션 실행하기", type="primary")

    # 시뮬레이션 계산 로직 함수
    def run_simulation(antler, stamina, total_rounds):
        energy = float(stamina)
        energy_history = [energy]
        intimidations, defeats = 0, 0

        weight_cost = antler * 0.18
        challenge_prob = max(0.10, 0.90 - (antler / 100.0) * 0.75)

        for r in range(1, total_rounds + 1):
            if energy <= 0:
                break
            # 유지 비용 소모
            energy -= weight_cost

            # 라이벌 도전 판정
            if np.random.rand() < challenge_prob:
                damage = max(5.0, 40.0 - (antler * 0.35))
                energy -= damage
                defeats += 1
            else:
                intimidations += 1

            energy = max(0.0, energy)
            energy_history.append(energy)

        return energy, energy_history, intimidations, defeats

    if run_sim or "sim_done" not in st.session_state:
        final_energy, history, intim, fights = run_simulation(
            antler_size, stamina_input, rounds_input
        )
        st.session_state.sim_result = (final_energy, history, intim, fights)
        st.session_state.sim_done = True

    final_energy, history, intim, fights = st.session_state.sim_result

    # 결과 지표 카드 출력
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        if final_energy > 0:
            st.success("🎉 **생존 성공!**")
        else:
            st.error("☠️ **사멸 (체력 고갈)**")
    with m2:
        st.metric("남은 최종 체력", f"{final_energy:.1f} HP")
    with m3:
        st.metric("위협 성공 횟수", f"{intim} 회")
    with m4:
        st.metric("직접 충돌 횟수", f"{fights} 회")

    # Plotly 시각화 그래프
    df_chart = pd.DataFrame(
        {"라운드": list(range(len(history))), "체력(HP)": history}
    )
    fig = px.line(
        df_chart,
        x="라운드",
        y="체력(HP)",
        title=f"뿔 크기 [{antler_size}] 개체의 라운드별 체력 변화 추이",
        markers=True,
    )
    fig.add_hline(
        y=0, line_dash="dash", line_color="red", annotation_text="사멸 선"
    )
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 3. 작동 원리 및 수리 모델 탭
# ==========================================
with tab3:
    st.header("📐 핸디캡 원리의 수리적 모델링")

    st.markdown("""
    이 시뮬레이터는 두 가지 상충하는 비용과 이득의 **트레이드오프(Trade-off)** 관계를 수학적으로 반영합니다.
    """)

    col_m1, col_m2 = st.columns(2)

    with col_m1:
        st.subheader("1. 뿔 유지 비용 (Handicap Cost)")
        st.latex(r"C_{\text{weight}} = \text{Antler} \times 0.18")
        st.markdown(
            "- 뿔이 무거울수록 이동과 목 지탱에 드는 매 라운드 **기초 체력 소모가 증가**합니다."
        )

    with col_m2:
        st.subheader("2. 라이벌의 도전 확률 (Deterrence Effect)")
        st.latex(
            r"P_{\text{challenge}} = \max\left(0.10, 0.90 - \frac{\text{Antler}}{100} \times 0.75\right)"
        )
        st.markdown(
            "- 뿔이 거대할수록 라이벌이 상대의 강함을 직관적으로 인지하여 **싸움을 포기하고 도망칠 확률이 높아집니다.**"
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
