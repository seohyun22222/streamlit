import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="3D 사슴 핸디캡 원리 시뮬레이터",
    page_icon="🦌",
    layout="wide",
)

st.title("🦌 3D 핸디캡 원리 생태 시뮬레이터")
st.caption(
    "자연선택(Natural Selection)과 진화적으로 안정된 전략(ESS)의 3D 인터랙티브 실험실"
)

# 4가지 메인 탭 구성
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "💡 1. 탐구 동기",
        "🎬 2. 3D 리얼 애니메이션 시뮬레이션",
        "📐 3. 작동 원리 & 수리 모델",
        "📊 4. 결과 분석 & 고찰",
    ]
)

# ==========================================
# 1. 탐구 동기 탭 (정리된 핵심 요약)
# ==========================================
with tab1:
    st.markdown("### 📌 탐구의 핵심 질문 및 개요")

    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        #### 1. 자연선택: 완벽함이 아닌 '차선의 최적화'
        - 자연선택은 모든 생물을 완벽하게 만드는 전지전능한 설계도가 아닙니다.
        - 주어진 환경과 유전적 제약 안에서 유전자를 다음 세대에 더 많이 남기기 위한 **상대적 필터링 메커니즘**입니다.
        
        #### 2. 핸디캡 원리: '손해'를 통한 신뢰의 증명
        - 사슴의 거대한 뿔처럼 생존에 방해가 되는 과시적 낭비는 가짜가 감히 흉내 낼 수 없는 극단적인 비용을 치름으로써, **자신의 유전적 우수성을 증명하는 확실한 방법**이 됩니다.
        """)

    with col2:
        st.success("""
        #### 3. 진화적으로 안정된 전략 (ESS): 비용과 이득의 수학적 균형
        - 뿔이 너무 작으면 싸움 비용이 늘어나고, 너무 크면 유지 에너지가 고갈됩니다.
        - 자연선택은 이 두 비용 사이에서 생존 효율을 극대화하는 **최적의 타협점**을 찾아내며, 이것이 바로 진화가 만들어낸 정교한 균형 감각입니다.
        """)
        st.markdown(
            "👉 **'🎬 2. 3D 리얼 애니메이션 시뮬레이션'** 탭에서 움직이는 사슴을 직접 확인해 보세요!"
        )

# ==========================================
# 2. 3D 리얼 애니메이션 시뮬레이션 탭
# ==========================================
with tab2:
    st.sidebar.header("⚙️ 시뮬레이션 조작")
    antler_size = st.sidebar.slider(
        "내 사슴 뿔 크기 (Handicap Level)",
        min_value=0,
        max_value=100,
        value=50,
        step=5,
    )
    stamina_input = st.sidebar.slider("기초 체력 (HP)", 50, 300, 150, 10)
    rounds_input = st.sidebar.slider("영역 다툼 횟수", 5, 30, 15, 5)

    # VPython WebGL 기반 동적 애니메이션 HTML 생성
    def render_3d_action_simulation(antler_val):
        scale = 0.2 + (antler_val / 100.0) * 1.5

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
                        width: 780, 
                        height: 460, 
                        background: vec(0.1, 0.14, 0.18),
                        center: vec(0, 1.2, 0),
                        forward: vec(-0.8, -0.3, -1)
                    }});
                    
                    // 넓은 풀밭 바닥
                    var ground = box({{pos: vec(0,-0.1,0), size: vec(25, 0.2, 25), color: vec(0.22, 0.48, 0.22)}});
                    
                    // 사슴 생성 함수
                    function createDeer(posX, posZ, antlerScale, isRival) {{
                        var bodyColor = isRival ? vec(0.45, 0.25, 0.1) : vec(0.65, 0.38, 0.15);
                        var antlerColor = isRival ? vec(0.7, 0.6, 0.4) : vec(0.9, 0.8, 0.5);
                        
                        var deerGroup = [];
                        var body = cylinder({{pos: vec(posX-0.8, 1.2, posZ), axis: vec(1.6, 0, 0), radius: 0.5, color: bodyColor}});
                        var head = sphere({{pos: vec(posX+1.0, 2.0, posZ), radius: 0.35, color: bodyColor}});
                        
                        // 다리 4개
                        var l1 = cylinder({{pos: vec(posX-0.6, 1.2, posZ+0.3), axis: vec(0, -1.2, 0), radius: 0.09, color: bodyColor}});
                        var l2 = cylinder({{pos: vec(posX-0.6, 1.2, posZ-0.3), axis: vec(0, -1.2, 0), radius: 0.09, color: bodyColor}});
                        var l3 = cylinder({{pos: vec(posX+0.5, 1.2, posZ+0.3), axis: vec(0, -1.2, 0), radius: 0.09, color: bodyColor}});
                        var l4 = cylinder({{pos: vec(posX+0.5, 1.2, posZ-0.3), axis: vec(0, -1.2, 0), radius: 0.09, color: bodyColor}});
                        
                        // 뿔 생성
                        var a1 = cylinder({{pos: vec(posX+1.0, 2.2, posZ+0.15), axis: vec(0.2*antlerScale, 0.8*antlerScale, 0.4*antlerScale), radius: 0.06, color: antlerColor}});
                        var a2 = cylinder({{pos: vec(posX+1.0, 2.2, posZ-0.15), axis: vec(0.2*antlerScale, 0.8*antlerScale, -0.4*antlerScale), radius: 0.06, color: antlerColor}});
                        
                        return {{body: body, head: head, l1: l1, l2: l2, l3: l3, l4: l4, a1: a1, a2: a2, posX: posX, posZ: posZ}};
                    }}
                    
                    // 내 사슴 (왼쪽) & 라이벌 사슴 (오른쪽)
                    var myDeer = createDeer(-3, 0, {scale}, false);
                    var rivalDeer = createDeer(5, 0, 0.8, true); // 라이벌은 일정 크기의 뿔 보유
                    
                    var state = "APPROACH"; // APPROACH, INTERACT, RETREAT, FIGHT
                    var t = 0;
                    var actionTimer = 0;
                    
                    var myAntlerVal = {antler_val};
                    
                    while (true) {{
                        await rate(30);
                        t += 0.1;
                        actionTimer += 1;
                        
                        // 보행 애니메이션 (다리 움직임)
                        var legMove = Math.sin(t * 3) * 0.2;
                        myDeer.l1.axis = vec(legMove, -1.2, 0);
                        myDeer.l2.axis = vec(-legMove, -1.2, 0);
                        rivalDeer.l1.axis = vec(legMove, -1.2, 0);
                        rivalDeer.l2.axis = vec(-legMove, -1.2, 0);
                        
                        // 상태 머신 (행동 제어)
                        if (state === "APPROACH") {{
                            // 서로에게 다가옴
                            if (myDeer.posX < -1.2) {{
                                myDeer.posX += 0.05;
                                myDeer.body.pos.x += 0.05;
                                myDeer.head.pos.x += 0.05;
                                myDeer.l1.pos.x += 0.05; myDeer.l2.pos.x += 0.05;
                                myDeer.l3.pos.x += 0.05; myDeer.l4.pos.x += 0.05;
                                myDeer.a1.pos.x += 0.05; myDeer.a2.pos.x += 0.05;
                            }}
                            if (rivalDeer.posX > 1.2) {{
                                rivalDeer.posX -= 0.05;
                                rivalDeer.body.pos.x -= 0.05;
                                rivalDeer.head.pos.x -= 0.05;
                                rivalDeer.l1.pos.x -= 0.05; rivalDeer.l2.pos.x -= 0.05;
                                rivalDeer.l3.pos.x -= 0.05; rivalDeer.l4.pos.x -= 0.05;
                                rivalDeer.a1.pos.x -= 0.05; rivalDeer.a2.pos.x -= 0.05;
                            }}
                            if (actionTimer > 80) {{
                                state = "INTERACT";
                                actionTimer = 0;
                            }}
                        }} else if (state === "INTERACT") {{
                            // 대치 상태: 머리 흔들며 서로의 뿔을 확인
                            myDeer.head.pos.y = 2.0 + Math.sin(t*2)*0.08;
                            rivalDeer.head.pos.y = 2.0 + Math.cos(t*2)*0.08;
                            
                            if (actionTimer > 50) {{
                                // 뿔 크기에 따른 판정 (뿔이 크면 라이벌 도망, 작으면 충돌)
                                if (myAntlerVal >= 40) {{
                                    state = "RETREAT"; // 위협 성공 -> 라이벌 도망
                                }} else {{
                                    state = "FIGHT"; // 뿔이 작음 -> 부딪힘
                                }}
                                actionTimer = 0;
                            }}
                        }} else if (state === "RETREAT") {{
                            // 라이벌이 겁먹고 뒤로 도망침
                            rivalDeer.body.pos.x += 0.08;
                            rivalDeer.head.pos.x += 0.08;
                            rivalDeer.l1.pos.x += 0.08; rivalDeer.l2.pos.x += 0.08;
                            rivalDeer.l3.pos.x += 0.08; rivalDeer.l4.pos.x += 0.08;
                            rivalDeer.a1.pos.x += 0.08; rivalDeer.a2.pos.x += 0.08;
                        }} else if (state === "FIGHT") {{
                            // 서로 뿔을 맞대고 쿵쿵거리며 싸움
                            var fightShake = Math.sin(t * 10) * 0.06;
                            myDeer.head.pos.x = -0.2 + fightShake;
                            rivalDeer.head.pos.x = 0.2 - fightShake
