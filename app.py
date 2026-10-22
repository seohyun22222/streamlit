import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="거대한 뿔의 역설: 핸디캡 원리 시뮬레이터",
    page_icon="🦌",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🦌 거대한 뿔의 역설: 핸디캡 원리(Handicap Principle) 시뮬레이터")
st.markdown("""
자연계의 사슴이나 공작은 생존에 전혀 도움 되지 않는 거대하고 무거운 **'뿔'**이나 **'깃털'**을 왜 진화시켰을까요?  
이 시뮬레이터는 **"손해를 감수하는 과시(Handicap)가 어떻게 불필요한 싸움을 막아 생존율을 높이는지"**를 수학적 모델과 그래프로 보여줍니다.
""")

st.markdown("---")

# 2. 사이드바 설정 파라미터
st.sidebar.header("⚙️ 실험 변수 설정")

# 실행 모드 선택
sim_mode = st.sidebar.radio(
    "실험 모드 선택",
    ["단일 개체 심층 실험", "3가지 뿔 크기 비교 실험"],
    help="단일 개체의 결과를 정밀하게 모니터링하거나, 뿔 크기별 개체를 동시에 비교할 수 있습니다.",
)

st.sidebar.markdown("---")

if sim_mode == "단일 개체 심층 실험":
    antler_size = st.sidebar.slider(
        "내 뿔의 크기 (Handicap Level)",
        min_value=0,
        max_value=100,
        value=50,
        step=5,
        help="0: 아주 작음 / 50: 적정 수준 / 100: 극단적으로 거대함",
    )
else:
    antler_size = 50  # 기본값 지정

base_stamina = st.sidebar.number_input(
    "기초 체력 (Initial Stamina)",
    min_value=50,
    max_value=300,
    value=150,
    step=10,
    help="개체가 시작할 때 보유한 총 에너지",
)

rounds = st.sidebar.slider(
    "영역 다툼 횟수 (Rounds)",
    min_value=5,
    max_value=50,
    value=20,
    step=5,
    help="숲에서 경쟁자와 조우하여 영역을 다투는 총 라운드 수",
)

st.sidebar.markdown("---")
run_sim = st.sidebar.button("🚀 시뮬레이션 실행", type="primary")


# 3. 핵심 시뮬레이션 알고리즘 함수
def simulate_deer(antler, stamina, total_rounds, seed=None):
    if seed is not None:
        np.random.seed(seed)

    energy = float(stamina)
    energy_history = [energy]
    fight_records = []
    intimidations = 0
    defeats = 0

    # 뿔 유지 비용 (무거울수록 매 라운드 에너지 소모)
    weight_cost = antler * 0.18

    # 라이벌이 시비를 걸 확률 (뿔이 클수록 라이벌이 위협을 느껴 도전 포기)
    challenge_prob = max(0.10, 0.90 - (antler / 100.0) * 0.75)

    for r in range(1, total_rounds + 1):
        if energy <= 0:
            break

        # 1) 기초 뿔 지탱 및 이동 에너지 소모
        energy -= weight_cost

        # 2) 라이벌 조우 및 반응 판정
        if np.random.rand() < challenge_prob:
            # 라이벌이 도전함 -> 몸싸움 발생!
            fight_damage = max(5.0, 40.0 - (antler * 0.35))
            energy -= fight_damage
            defeats += 1
            fight_records.append(
                f"라운드 {r:02d}: ⚔️ 라이벌이 도전해옴! (충돌 발생, -{fight_damage:.1f} HP)"
            )
        else:
            # 라이벌이 뿔을 보고 지레 겁먹음 -> 무혈입성
            intimidations += 1
            fight_records.append(
                f"라운드 {r:02d}: 🛡️ 거대한 뿔에 도망침! (위협 성공, 싸움 회피)"
            )

        energy = max(0.0, energy)
        energy_history.append(energy)

    return {
        "survived": energy > 0,
        "final_energy": energy,
        "energy_history": energy_history,
        "intimidations": intimidations,
        "defeats": defeats,
        "records": fight_records,
    }


# 4. 메인 대시보드 레이아웃
if sim_mode == "단일 개체 심층 실험":
    col_info, col_status = st.columns([1, 1])

    with col_info:
        st.subheader("💡 핸디캡 원리 (Handicap Principle)")
        st.info("""
        - **뿔이 너무 작은 사슴 (0~25):** 뿔이 가벼워 평소 체력은 아끼지만, 라이벌들이 만만하게 보고 매 라운드 싸움을 걸어와 **전투 피로로 사멸**합니다.
        - **뿔이 너무 큰 사슴 (75~100):** 라이벌은 절대 안 건드리지만, 그 거대한 뿔을 지탱하느라 **스스로 굶어 죽거나 탈진**합니다.
        - **적정 핸디캡 사슴 (35~65):** 최소한의 에너지 낭비로 최대의 위협 효과를 얻어 **자연선택에 의해 생존(ESS)**합니다.
        """)

    with col_status:
        st.subheader("📊 선택한 개체 예상 스펙")
        st.write(
            f"- **라운드당 뿔 유지 비용:** `-{antler_size * 0.18:.1f} HP`"
        )
        st.write(
            f"- **라이벌의 도전에 직면할 확률:** `{max(10, int((0.90 - (antler_size / 100.0) * 0.75) * 100))}%`"
        )
        st.write(
            f"- **싸움 발생 시 데미지:** `-{max(5.0, 40.0 - (antler_size * 0.35)):.1f} HP`"
        )

    if run_sim:
        st.markdown("---")
        st.subheader("🎬 시뮬레이션 결과 리포트")

        res = simulate_deer(antler_size, base_stamina, rounds)

        # 결과 메트릭 카드
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            if res["survived"]:
                st.success("🎉 **영역 수성 성공!**")
            else:
                st.error("☠️ **에너지 고갈 사멸**")
        with m2:
            st.metric("남은 최종 에너지", f"{res['final_energy']:.1f} HP")
        with m3:
            st.metric("라이벌 위협 회피 횟수", f"{res['intimidations']} 회")
        with m4:
            st.metric("직접 충돌 횟수", f"{res['defeats']} 회")

        # 에너지 변화 추이 그래프 (Plotly)
        df_chart = pd.DataFrame(
            {
                "라운드": list(range(len(res["energy_history"]))),
                "잔여 에너지(HP)": res["energy_history"],
            }
        )

        fig = px.line(
            df_chart,
            x="라운드",
            y="잔여 에너지(HP)",
            title="라운드 진행에 따른 사슴의 잔여 체력 추이",
            markers=True,
            line_shape="spline",
            color_discrete_sequence=["#2E7D32" if res["survived"] else "#C62828"],
        )
        fig.add_hline(
            y=0,
            line_dash="dash",
            line_color="red",
            annotation_text="생존 한계선 (0 HP)",
        )
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

        # 상세 로그 보기
        with st.expander("🔍 라운드별 상세 이벤트 기록 보기"):
            for rec in res["records"]:
                st.write(rec)

        # 학술적 분석 피드백
        st.markdown("---")
        st.subheader("🧬 진화생물학적 진단")
        if antler_size < 30:
            st.warning(
                "⚠️ **핸디캡 부족 (Under-Handicapped):** 뿔이 너무 작아 강함을 증명하지 못했습니다. 끊임없는 라이벌의 도전으로 인해 전투 손실이 극대화되었습니다."
            )
        elif antler_size > 70:
            st.warning(
                "⚠️ **과도한 핸디캡 (Over-Handicapped):** 라이벌들은 제압했으나, 자신의 신체 장식(뿔) 무게를 견디지 못하고 자멸한 케이스입니다."
            )
        else:
            st.success(
                "✨ **최적의 진화적 안정 전략 (Evolutionary Stable Strategy):** 핸디캡의 기회비용과 위협 이득이 완벽한 균형을 이루어 자연선택에 의해 우세종이 되었습니다!"
            )

else:  # 3가지 뿔 크기 비교 실험 모드
    st.info(
        "💡 **비교 실험 모드:** 동일한 환경 조건에서 [작은 뿔(15)], [적정 뿔(50)], [거대한 뿔(85)]을 가진 세 개체의 생존 경쟁을 동시에 비교합니다."
    )

    if run_sim:
        st.markdown("---")
        st.subheader("📊 3가지 진화 그룹 대조 실험 결과")

        seed_val = np.random.randint(1, 10000)
        res_small = simulate_deer(15, base_stamina, rounds, seed=seed_val)
        res_med = simulate_deer(50, base_stamina, rounds, seed=seed_val)
        res_large = simulate_deer(85, base_stamina, rounds, seed=seed_val)

        # 3가지 그룹 비교 차트
        max_len = max(
            len(res_small["energy_history"]),
            len(res_med["energy_history"]),
            len(res_large["energy_history"]),
        )

        df_comp = pd.DataFrame(
            {
                "라운드": list(range(max_len)),
                "작은 뿔 (15)": res_small["energy_history"]
                + [0] * (max_len - len(res_small["energy_history"])),
                "적정 뿔 (50)": res_med["energy_history"]
                + [0] * (max_len - len(res_med["energy_history"])),
                "거대한 뿔 (85)": res_large["energy_history"]
                + [0] * (max_len - len(res_large["energy_history"])),
            }
        )

        fig_comp = go.Figure()
        fig_comp.add_trace(
            go.Scatter(
                x=df_comp["라운드"],
                y=df_comp["작은 뿔 (15)"],
                mode="lines+markers",
                name="작은 뿔 (15)",
                line=dict(color="#FF9800"),
            )
        )
