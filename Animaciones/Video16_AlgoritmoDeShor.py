from manim import *
import numpy as np


class AlgoritmoDeShor(Scene):
    def construct(self):
        title = self.top_text("Algoritmo de Shor").scale(1.05)
        self.play(Write(title), run_time=0.9)

        curve_panel = self.curve_panel().move_to(LEFT * 2.95 + UP * 0.45)
        lock = self.lock_icon().move_to(RIGHT * 2.85 + UP * 0.35)
        bottom = self.bottom_text("En ECC, el problema duro es: dado Q = kP, recuperar k.")

        self.play(FadeIn(curve_panel), Create(lock), Write(bottom), run_time=2.0)
        self.wait(4.8)

        narrative_1 = self.top_text("Un ordenador clásico solo ve muchos saltos discretos por el grupo.")
        walk = self.discrete_walk().move_to(LEFT * 2.95 + UP * 0.45)
        bottom_1 = self.bottom_text("la estructura está escondida dentro de una secuencia enorme", color=WHITE)
        self.play(Transform(title, narrative_1), ReplacementTransform(bottom, bottom_1), ReplacementTransform(curve_panel, walk), run_time=1.3)
        self.play(Indicate(walk, color=YELLOW, scale_factor=1.03), run_time=1.0)
        self.wait(5.0)

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1.8, 2.8, 1],
            x_length=8.2,
            y_length=4.6,
            axis_config={"include_tip": False, "stroke_color": GRAY},
        ).shift(UP * 0.15)
        grid = self.add_grid(axes)
        waves = self.quantum_waves(axes)

        quantum_box = self.info_box(["ordenador cuántico", "nuevo modelo", "de cálculo"], BLUE).move_to(RIGHT * 2.75 + UP * 1.95)
        quantum_box.set_z_index(20)
        narrative_2 = self.top_text("Un ordenador cuántico cambia las reglas: el algoritmo de Shor evalúa todos los saltos a la vez.")
        bottom_2 = self.bottom_text("superposición cuántica: muchas posibilidades interfieren como ondas", color=GREEN, font="Cambria Math")
        self.play(
            Transform(title, narrative_2),
            ReplacementTransform(bottom_1, bottom_2),
            FadeOut(walk),
            FadeOut(lock),
            Create(grid),
            Create(axes),
            FadeIn(quantum_box),
            LaggedStart(*[Create(wave) for wave in waves], lag_ratio=0.12),
            run_time=2.0,
        )
        self.wait(5.5)

        periodic_marks = VGroup()
        for x in [-3.0, -1.5, 0.0, 1.5, 3.0]:
            line = DashedLine(axes.c2p(x, -1.25), axes.c2p(x, 2.35), color=YELLOW, stroke_width=2, dash_length=0.10)
            line.set_z_index(5)
            periodic_marks.add(line)
        period_label = Text("periodo r", font="Cambria Math", color=YELLOW).scale(0.46)
        period_label.move_to(UP * 2.20 + LEFT * 2.10)

        narrative_3 = self.top_text("La periodicidad queda codificada en las fases de esas ondas.")
        bottom_3 = self.bottom_text("el secreto k se esconde en una repetición: encontrar el periodo r", color=WHITE)
        self.play(Transform(title, narrative_3), ReplacementTransform(bottom_2, bottom_3), FadeIn(periodic_marks), Write(period_label), run_time=1.3)
        self.play(Indicate(periodic_marks, color=YELLOW, scale_factor=1.02), run_time=1.0)
        self.wait(5.5)

        spectrum = self.spectrum(axes)
        qft_box = self.info_box(["QFT", "transformada cuántica", "de Fourier"], GREEN).move_to(RIGHT * 2.65 + DOWN * 1.75)
        qft_box.set_z_index(20)
        narrative_4 = self.top_text("La transformada cuántica de Fourier convierte el periodo en picos medibles.")
        bottom_4 = self.bottom_text("las ondas se cancelan casi siempre y se refuerzan en posiciones especiales", color=GREEN, font="Cambria Math")
        self.play(Transform(title, narrative_4), ReplacementTransform(bottom_3, bottom_4), FadeOut(period_label), FadeOut(quantum_box), FadeIn(qft_box), run_time=1.0)
        self.play(ReplacementTransform(waves, spectrum), FadeOut(periodic_marks), run_time=1.6)
        self.play(Indicate(spectrum[2], color=GREEN, scale_factor=1.08), run_time=1.0)
        self.wait(5.8)

        period_card = self.value_card("periodo r", YELLOW, width=2.35, scale=0.52).move_to(LEFT * 2.20 + UP * 0.15)
        key_card = self.value_card("clave k", PURPLE, width=2.35, scale=0.52).move_to(RIGHT * 2.20 + UP * 0.15)
        arrow = Arrow(period_card.get_right(), key_card.get_left(), buff=0.16, color=GREEN, stroke_width=4)
        arrow_label = Text("álgebra clásica", font="Cambria Math", color=GREEN).scale(0.36)
        arrow_label.next_to(arrow, UP, buff=0.12)

        narrative_5 = self.top_text("Con suficiente información sobre el periodo, el resto es álgebra clásica.")
        bottom_5 = self.bottom_text("periodo r  →  relación oculta  →  clave k", color=GREEN, font="Cambria Math", scale=0.64, y=-2.55)
        self.play(
            Transform(title, narrative_5),
            ReplacementTransform(bottom_4, bottom_5),
            FadeOut(qft_box),
            FadeOut(grid),
            FadeOut(axes),
            FadeOut(spectrum),
            FadeIn(period_card),
            Create(arrow),
            Write(arrow_label),
            FadeIn(key_card),
            run_time=1.4,
        )
        self.play(Flash(key_card.get_center(), color=PURPLE, flash_radius=0.75), run_time=0.9)
        self.wait(5.5)

        broken_lock = self.broken_lock().scale(1.15).move_to(LEFT * 2.35 + UP * 0.40)
        final_explain = self.info_box(
            ["Shor recupera k", "el candado ECDLP queda abierto", "con hardware cuántico grande"],
            RED,
            width=4.20,
            height=1.42,
        ).move_to(RIGHT * 2.05 + UP * 0.40)
        final_arrow = Arrow(broken_lock.get_right(), final_explain.get_left(), buff=0.18, color=RED, stroke_width=4)
        final_bottom = self.bottom_text("amenaza cuántica: migrar hacia criptografía post-cuántica", color=RED, font="Cambria Math", scale=0.66, y=-2.55)
        narrative_6 = self.top_text("Por eso Shor amenaza RSA y ECC si existen ordenadores cuánticos grandes.")
        self.play(
            Transform(title, narrative_6),
            ReplacementTransform(bottom_5, final_bottom),
            FadeOut(period_card),
            FadeOut(arrow),
            FadeOut(arrow_label),
            FadeOut(key_card),
            FadeIn(broken_lock),
            Create(final_arrow),
            FadeIn(final_explain),
            run_time=1.3,
        )
        self.play(Indicate(VGroup(broken_lock, final_arrow, final_explain), color=RED, scale_factor=1.03), run_time=1.0)
        self.wait(6.0)

    def top_text(self, text, scale=0.60):
        mob = Text(text, font="Cambria").scale(scale)
        if mob.width > 12.4:
            mob.scale_to_fit_width(12.4)
        mob.to_edge(UP)
        return mob

    def bottom_text(self, text, color=WHITE, font="Cambria", scale=0.58, y=-2.92):
        mob = Text(text, font=font, color=color).scale(scale)
        if mob.width > 11.8:
            mob.scale_to_fit_width(11.8)
        mob.move_to(UP * y)
        return mob

    def curve_panel(self):
        axes = Axes(
            x_range=[-2.3, 2.3, 1],
            y_range=[-1.7, 1.9, 1],
            x_length=3.4,
            y_length=2.6,
            axis_config={"include_tip": False, "stroke_color": GRAY},
        )
        curve = axes.plot_implicit_curve(lambda x, y: y**2 - (x**3 - x + 0.65), color=BLUE, stroke_width=3)
        p = Dot(axes.c2p(-0.85, self.curve_y(-0.85)), color=YELLOW, radius=0.070)
        q = Dot(axes.c2p(0.70, self.curve_y(0.70)), color=RED, radius=0.070)
        p_label = Text("P", font="Cambria Math", color=YELLOW).scale(0.34).next_to(p, UP, buff=0.06)
        q_label = Text("Q=kP", font="Cambria Math", color=RED).scale(0.30).next_to(q, UP, buff=0.06)
        return VGroup(axes, curve, p, q, p_label, q_label)

    def curve_y(self, x):
        return np.sqrt(max(0, x**3 - x + 0.65))

    def lock_icon(self):
        body = RoundedRectangle(
            corner_radius=0.08,
            width=1.35,
            height=0.86,
            color=RED,
            fill_color="#240B12",
            fill_opacity=0.92,
            stroke_width=4,
        )
        arc = Arc(radius=0.48, start_angle=0, angle=PI, color=RED, stroke_width=4)
        arc.next_to(body, UP, buff=-0.18)
        label = Text("ECDLP", font="Cambria Math", color=RED).scale(0.36)
        label.next_to(body, DOWN, buff=0.12)
        return VGroup(body, arc, label)

    def broken_lock(self):
        body = RoundedRectangle(
            corner_radius=0.08,
            width=1.55,
            height=0.96,
            color=RED,
            fill_color="#240B12",
            fill_opacity=0.92,
            stroke_width=4,
        )
        broken_arc = VGroup(
            Line(LEFT * 0.55 + UP * 0.65, LEFT * 0.05 + UP * 1.10, color=GREEN, stroke_width=5),
            Line(RIGHT * 0.55 + UP * 0.65, RIGHT * 0.10 + UP * 0.90, color=GREEN, stroke_width=5),
        )
        label = Text("ECDLP", font="Cambria Math", color=RED).scale(0.42)
        label.move_to(body)
        crack = Text("k", font="Cambria Math", color=PURPLE).scale(0.55).next_to(body, DOWN, buff=0.16)
        return VGroup(body, broken_arc, label, crack)

    def discrete_walk(self):
        dots = VGroup()
        arrows = VGroup()
        positions = [
            LEFT * 1.25 + DOWN * 0.70,
            LEFT * 0.65 + UP * 0.55,
            RIGHT * 0.10 + DOWN * 0.20,
            RIGHT * 0.70 + UP * 0.80,
            RIGHT * 1.30 + DOWN * 0.45,
        ]
        for index, position in enumerate(positions):
            color = YELLOW if index == 0 else BLUE
            dots.add(Dot(position, color=color, radius=0.075))
            if index > 0:
                arrows.add(Arrow(positions[index - 1], position, buff=0.15, color=GREEN, stroke_width=3, max_tip_length_to_length_ratio=0.12))
        label = Text("P, 2P, 3P, ...", font="Cambria Math", color=YELLOW).scale(0.38)
        label.next_to(dots, DOWN, buff=0.25)
        return VGroup(arrows, dots, label)

    def add_grid(self, axes):
        lines = VGroup()
        for x in np.arange(-4, 4.1, 1):
            lines.add(Line(axes.c2p(x, -1.4), axes.c2p(x, 2.6), color=GRAY, stroke_width=1, stroke_opacity=0.16))
        for y in np.arange(-1, 2.1, 1):
            lines.add(Line(axes.c2p(-4, y), axes.c2p(4, y), color=GRAY, stroke_width=1, stroke_opacity=0.16))
        return lines

    def quantum_waves(self, axes):
        colors = [YELLOW, RED, BLUE, PURPLE, GREEN]
        waves = VGroup()
        for index, phase in enumerate([0.0, 0.7, 1.6, 2.4, 3.1]):
            wave = axes.plot(
                lambda x, ph=phase: 0.34 * np.sin(4 * x + ph) + 0.18 * np.sin(7 * x - ph) + 0.14 * index,
                color=colors[index],
                stroke_width=3,
            )
            waves.add(wave)
        return waves

    def spectrum(self, axes):
        baseline = -0.35
        peak_y = 1.90
        pts = [axes.c2p(-4.0, baseline)]
        for peak_x in [-2.2, 0.35, 2.7]:
            pts.extend(
                [
                    axes.c2p(peak_x - 0.33, baseline),
                    axes.c2p(peak_x, peak_y),
                    axes.c2p(peak_x + 0.33, baseline),
                ]
            )
        pts.append(axes.c2p(4.0, baseline))
        spectrum_line = VMobject(color=GREEN, stroke_width=5).set_points_as_corners(pts)
        peaks = VGroup(
            Dot(axes.c2p(-2.2, peak_y), color=GREEN, radius=0.065),
            Dot(axes.c2p(0.35, peak_y), color=GREEN, radius=0.065),
            Dot(axes.c2p(2.7, peak_y), color=GREEN, radius=0.065),
        )
        label = Text("picos del periodo", font="Cambria Math", color=GREEN).scale(0.42)
        label.move_to(LEFT * 2.30 + UP * 2.48)
        return VGroup(spectrum_line, peaks, label)

    def info_box(self, lines, color, width=2.45, height=1.20):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=width,
            height=height,
            color=color,
            fill_color="#151515",
            fill_opacity=0.92,
        )
        text = VGroup(
            *[
                Text(line, font="Cambria Math" if index == 0 else "Cambria", color=color if index == 0 else WHITE).scale(
                    0.42 if index == 0 else 0.28
                )
                for index, line in enumerate(lines)
            ]
        ).arrange(DOWN, buff=0.07)
        text.move_to(box)
        return VGroup(box, text)

    def value_card(self, text, color, width=1.85, scale=0.42):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=width,
            height=0.82,
            color=color,
            fill_color="#151515",
            fill_opacity=0.92,
        )
        label = Text(text, font="Cambria Math", color=color).scale(scale)
        label.move_to(box)
        return VGroup(box, label)
