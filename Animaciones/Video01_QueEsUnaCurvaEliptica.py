from manim import *
import numpy as np

class QueEsUnaCurvaEliptica(Scene):
    def construct(self):
        # 1. Configuración de Ejes y Título
        title = Tex("¿Qué es una Curva Elíptica?").to_edge(UP)
        self.play(Write(title))

        # Ejes fijos, centrados y ligeramente desplazados hacia abajo para dejar espacio al título
        axes = Axes(
            x_range=[-4, 5, 1],
            y_range=[-6, 6, 1],
            x_length=8.5,
            y_length=5.5,
            axis_config={"include_tip": False}
        ).shift(DOWN * 0.2)

        # Trackers para los parámetros a y b
        a = ValueTracker(-1.0)
        b = ValueTracker(1.0)

        def elliptic_curve_mobject(a_value, b_value, color):
            return axes.plot_implicit_curve(
                lambda x, y: y**2 - x**3 - a_value * x - b_value,
                color=color,
                stroke_width=3,
            )

        # Curva inicial y^2 = x^3 - x + 1, como en DobladoDePuntos.
        curve = elliptic_curve_mobject(a.get_value(), b.get_value(), BLUE)

        # 2. Fórmulas en una zona inferior compacta, fuera del área de los ejes
        eq_general = (
            MathTex("y^2 = x^3 + a x + b")
            .scale(0.75)
            .to_edge(DOWN, buff=0.72)
            .shift(LEFT * 2.15)
        )
        
        # DecimalNumber evita recompilar LaTeX en cada frame al animar los valores.
        params_text = VGroup(
            Text("a =", font="Cambria Math", slant=ITALIC, color=YELLOW).scale(0.5),
            DecimalNumber(a.get_value(), num_decimal_places=2, color=YELLOW).scale(0.6),
            Text("b =", font="Cambria Math", slant=ITALIC, color=YELLOW).scale(0.5),
            DecimalNumber(b.get_value(), num_decimal_places=2, color=YELLOW).scale(0.6),
        )
        params_text[1].add_updater(lambda m: m.set_value(a.get_value()))
        params_text[3].add_updater(lambda m: m.set_value(b.get_value()))

        def update_params_text(mob):
            mob.arrange(RIGHT, buff=0.11)
            mob.next_to(eq_general, RIGHT, buff=0.55)

        params_text.add_updater(update_params_text)
        update_params_text(params_text)

        self.play(Create(axes), Create(curve), run_time=2)
        self.play(Write(eq_general))
        self.play(FadeIn(params_text))
        self.wait(1)

        narrative_1 = Text(
            "Una curva elíptica es el conjunto de puntos que cumple esta ecuación.",
            font="Cambria",
        ).scale(0.42).to_edge(UP)
        self.play(Transform(title, narrative_1))
        self.wait(1)

        # 3. Mutación de parámetros
        narrative_2 = Tex("Los parámetros $a$ y $b$ determinan la forma exacta de la curva.").scale(0.85).to_edge(UP)
        self.play(Transform(title, narrative_2))
        
        curve_color = [BLUE]

        def update_curve(mob):
            mob.become(elliptic_curve_mobject(a.get_value(), b.get_value(), curve_color[0]))

        def animate_parameters_to(a_value, b_value, color=BLUE, run_time=3):
            curve_color[0] = color
            curve.add_updater(update_curve)
            self.play(
                a.animate.set_value(a_value),
                b.animate.set_value(b_value),
                run_time=run_time,
                rate_func=smooth,
            )
            curve.remove_updater(update_curve)
            curve.become(elliptic_curve_mobject(a_value, b_value, color))

        # Hacemos variar la forma sin pasar cerca de b = 0, donde la curva cruza el origen.
        animate_parameters_to(-0.4, 1.4, run_time=3)
        animate_parameters_to(-1.5, 1.0, run_time=3)
        self.wait(1)

        # 4. El Discriminante y la regla de curva lisa
        narrative_3 = Tex("Regla vital en Criptografía: la curva debe ser \\textbf{lisa}.").scale(0.85).to_edge(UP)
        self.play(Transform(title, narrative_3))

        delta_eq = (
            MathTex("\\Delta = -16(4a^3 + 27b^2) \\neq 0", color=GREEN)
            .scale(0.72)
            .next_to(VGroup(eq_general, params_text), DOWN, buff=0.12)
        )
        self.play(Write(delta_eq))
        self.wait(2)

        # 5. Singularidad (El colapso matemático)
        narrative_4 = Tex("Si $\\Delta = 0$, la curva se rompe y crea un punto singular.").scale(0.85).to_edge(UP)
        self.play(Transform(title, narrative_4))

        delta_zero = MathTex("\\Delta = 0", color=RED).scale(0.72).move_to(delta_eq)
        
        # a=-3 y b=2 generan una singularidad exacta en x=1
        curve_color[0] = RED
        self.play(
            UpdateFromFunc(curve, update_curve),
            a.animate.set_value(-3.0),
            b.animate.set_value(2.0),
            ReplacementTransform(delta_eq, delta_zero),
            run_time=3
        )
        curve_color[0] = RED
        curve.become(elliptic_curve_mobject(-3.0, 2.0, RED))

        # Destacamos el error geométrico sin mover la cámara, usando elementos puros
        cusp_dot = Dot(axes.c2p(1, 0), color=YELLOW, radius=0.08)
        cusp_label = Tex("Cúspide", color=YELLOW).scale(0.8)
        cusp_label.next_to(cusp_dot, DOWN+RIGHT, buff=0.25).shift(RIGHT * 0.35)
        
        self.play(FadeIn(cusp_dot), Write(cusp_label))
        self.play(Flash(cusp_dot, color=YELLOW, flash_radius=0.6))
        self.wait(2)

        # 6. Conclusión
        narrative_5 = Tex("Las curvas con singularidades son vulnerables y no se usan en seguridad.").scale(0.85).to_edge(UP)
        self.play(Transform(title, narrative_5))
        self.wait(3)
