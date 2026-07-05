from manim import *
import numpy as np


class AtaqueASIDH(Scene):
    def construct(self):
        title = self.top_text("Ataque a SIDH").scale(1.04)
        self.play(Write(title), run_time=0.9)

        graph = self.big_graph().move_to(ORIGIN + UP * 0.15)
        secret_path = self.secret_path(graph, [0, 5, 6, 7, 8, 13], color=GREEN)
        start_label = self.label_box("curva inicial", BLUE).move_to(LEFT * 3.15 + UP * 2.22)
        end_label = self.label_box("clave pública", PURPLE).move_to(RIGHT * 3.05 + DOWN * 1.95)
        start_arrow = Arrow(start_label.get_bottom(), graph[1][0].get_center(), buff=0.10, color=BLUE, stroke_width=3)
        end_arrow = Arrow(end_label.get_top(), graph[1][13].get_center(), buff=0.10, color=PURPLE, stroke_width=3)
        bottom = self.bottom_text("En SIDH, Alice y Bob caminan por un laberinto matematico para acordar una clave.")

        self.play(FadeIn(graph), Create(secret_path), FadeIn(start_label), FadeIn(end_label), Create(start_arrow), Create(end_arrow), Write(bottom), run_time=2.0)
        self.wait(5.0)

        aux_box = self.info_box(["información auxiliar", "puntos de torsión", "para poder compartir claves"], YELLOW, width=3.55, height=1.35).move_to(ORIGIN + UP * 0.10)
        aux_arrows = VGroup(
            Arrow(aux_box.get_left(), graph[1][6].get_center(), buff=0.12, color=YELLOW, stroke_width=3),
            Arrow(aux_box.get_right(), graph[1][8].get_center(), buff=0.12, color=YELLOW, stroke_width=3),
        )
        narrative_1 = self.top_text("Para poder mezclar sus resultados al final, debian publicar unos puntos de torsion extra.")
        bottom_1 = self.bottom_text("este mapa parcial era estrictamente necesario, pero resulto ser una debilidad fatal", color=YELLOW, font="Cambria Math")
        self.play(
            Transform(title, narrative_1),
            ReplacementTransform(bottom, bottom_1),
            FadeOut(start_label),
            FadeOut(end_label),
            FadeOut(start_arrow),
            FadeOut(end_arrow),
            graph.animate.set_opacity(0.35),
            secret_path.animate.set_opacity(0.35),
            FadeIn(aux_box),
            Create(aux_arrows),
            run_time=1.5,
        )
        self.wait(5.6)

        surface = self.surface_panel().move_to(ORIGIN + UP * 0.05)
        side_note = self.info_box(["2022", "Castryck-Decru", "curvas juntas en 2D"], RED, width=3.35, height=1.35).move_to(RIGHT * 2.70 + UP * 0.70)
        narrative_2 = self.top_text("El ataque de 2022 combino las curvas de ambos en un espacio de dos dimensiones.")
        bottom_2 = self.bottom_text("al mirarlas juntas, la superficie abeliana hizo visible parte del laberinto", color=WHITE)
        self.play(
            Transform(title, narrative_2),
            ReplacementTransform(bottom_1, bottom_2),
            FadeOut(graph),
            FadeOut(secret_path),
            FadeOut(aux_box),
            FadeOut(aux_arrows),
            FadeIn(surface),
            FadeIn(side_note),
            run_time=1.5,
        )
        self.wait(5.8)

        hidden_path = self.hidden_path().move_to(ORIGIN + UP * 0.05)
        attack_arrow = Arrow(LEFT * 2.90 + DOWN * 0.85, RIGHT * 2.80 + UP * 0.82, buff=0.10, color=RED, stroke_width=5)
        attack_label = Text("atajo", font="Cambria Math", color=RED).scale(0.50).next_to(attack_arrow, UP, buff=0.10)
        narrative_3 = self.top_text("Lo que parecía un laberinto resultó tener un atajo explotable.")
        bottom_3 = self.bottom_text("el ataque reconstruye el camino secreto a partir de los datos publicados", color=RED, font="Cambria Math")
        self.play(
            Transform(title, narrative_3),
            ReplacementTransform(bottom_2, bottom_3),
            FadeOut(surface),
            FadeOut(side_note),
            FadeIn(hidden_path),
            Create(attack_arrow),
            Write(attack_label),
            run_time=1.5,
        )
        self.play(Flash(attack_arrow.get_center(), color=RED, flash_radius=0.90), run_time=0.9)
        self.wait(5.8)

        broken = self.broken_scheme().move_to(LEFT * 2.35 + UP * 0.25)
        lesson = self.info_box(["lección", "no basta con una idea elegante", "también importa qué se publica"], GREEN, width=4.25, height=1.42).move_to(RIGHT * 2.05 + UP * 0.25)
        lesson_arrow = Arrow(broken.get_right(), lesson.get_left(), buff=0.16, color=GREEN, stroke_width=4)
        narrative_4 = self.top_text("SIDH no cayó por la palabra isogenia, sino por detalles concretos del protocolo.")
        bottom_4 = self.bottom_text("diseñar criptografía es controlar la matemática y la información expuesta", color=GREEN, font="Cambria Math")
        self.play(
            Transform(title, narrative_4),
            ReplacementTransform(bottom_3, bottom_4),
            FadeOut(hidden_path),
            FadeOut(attack_arrow),
            FadeOut(attack_label),
            FadeIn(broken),
            Create(lesson_arrow),
            FadeIn(lesson),
            run_time=1.5,
        )
        self.wait(6.0)

        timeline = self.timeline().move_to(ORIGIN + UP * 0.05)
        final_bottom = self.bottom_text("ECC enseña una idea central: estructura útil, pero siempre revisada con cuidado", color=GREEN, font="Cambria Math")
        narrative_5 = self.top_text("La evolución continúa: curvas, pairings, pruebas, cuántica e isogenias.")
        self.play(
            Transform(title, narrative_5),
            ReplacementTransform(bottom_4, final_bottom),
            FadeOut(broken),
            FadeOut(lesson_arrow),
            FadeOut(lesson),
            FadeIn(timeline),
            run_time=1.4,
        )
        self.play(Indicate(timeline, color=GREEN, scale_factor=1.02), run_time=1.0)
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

    def big_graph(self):
        points = [
            LEFT * 3.40 + UP * 1.35,
            LEFT * 2.15 + UP * 1.62,
            LEFT * 0.95 + UP * 1.20,
            RIGHT * 0.45 + UP * 1.65,
            RIGHT * 1.85 + UP * 1.15,
            LEFT * 2.55 + UP * 0.20,
            LEFT * 1.05 + UP * 0.10,
            RIGHT * 0.35 + UP * 0.30,
            RIGHT * 1.65 + DOWN * 0.20,
            RIGHT * 3.05 + UP * 0.20,
            LEFT * 1.85 + DOWN * 1.05,
            LEFT * 0.20 + DOWN * 0.95,
            RIGHT * 1.05 + DOWN * 1.35,
            RIGHT * 2.65 + DOWN * 1.15,
            LEFT * 3.25 + DOWN * 0.80,
        ]
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 4),
            (0, 5), (1, 5), (2, 6), (5, 6),
            (6, 7), (7, 8), (8, 9), (4, 9),
            (5, 14), (14, 10), (10, 11), (6, 10),
            (11, 12), (12, 13), (8, 13), (7, 12),
        ]
        lines = VGroup(*[Line(points[i], points[j], color=GRAY, stroke_width=2, stroke_opacity=0.55) for i, j in edges])
        dots = VGroup()
        for index, point in enumerate(points):
            color = BLUE if index == 0 else (PURPLE if index == 13 else WHITE)
            dots.add(Dot(point, color=color, radius=0.060))
        return VGroup(lines, dots)

    def secret_path(self, graph, indices, color=GREEN):
        dots = graph[1]
        path = VMobject(color=color, stroke_width=5)
        path.set_points_as_corners([dots[i].get_center() for i in indices])
        path.set_z_index(4)
        return path

    def label_box(self, text, color):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=1.70,
            height=0.50,
            color=color,
            fill_color="#151515",
            fill_opacity=0.92,
        )
        label = Text(text, font="Cambria", color=color).scale(0.27)
        label.move_to(box)
        return VGroup(box, label)

    def surface_panel(self):
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=6.25,
            y_length=3.60,
            axis_config={"include_tip": False, "stroke_color": GRAY},
        )
        waves = VGroup()
        for offset, color in [(-0.75, BLUE), (0.0, PURPLE), (0.75, GREEN)]:
            curve = axes.plot(lambda x, off=offset: 0.35 * np.sin(1.6 * x + off) + off, color=color, stroke_width=3)
            waves.add(curve)
        label = Text("superficie abeliana", font="Cambria Math", color=PURPLE).scale(0.46).next_to(axes, DOWN, buff=0.12)
        return VGroup(axes, waves, label)

    def hidden_path(self):
        graph = self.big_graph().scale(0.82)
        graph.set_opacity(0.32)
        path = self.secret_path(graph, [0, 5, 6, 7, 8, 13], color=GREEN)
        path.set_opacity(0.45)
        return VGroup(graph, path)

    def broken_scheme(self):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=2.40,
            height=1.25,
            color=RED,
            fill_color="#240B12",
            fill_opacity=0.92,
        )
        text = VGroup(
            Text("SIDH", font="Cambria Math", color=RED).scale(0.52),
            Text("roto en 2022", font="Cambria", color=WHITE).scale(0.32),
        ).arrange(DOWN, buff=0.08)
        text.move_to(box)
        cross = Cross(box, stroke_color=RED, stroke_width=5)
        return VGroup(box, text, cross)

    def timeline(self):
        labels = [
            ("curvas", BLUE),
            ("ECDH/ECDSA", GREEN),
            ("pairings", PURPLE),
            ("zkSNARKs", PURPLE),
            ("Shor", RED),
            ("isogenias", GREEN),
        ]
        points = VGroup()
        texts = VGroup()
        line = Line(LEFT * 4.65, RIGHT * 4.65, color=GRAY, stroke_width=2)
        for index, (label, color) in enumerate(labels):
            x = -4.25 + index * 1.70
            dot = Dot(np.array([x, 0, 0]), color=color, radius=0.065)
            text = Text(label, font="Cambria", color=color).scale(0.28)
            text.next_to(dot, UP if index % 2 == 0 else DOWN, buff=0.18)
            points.add(dot)
            texts.add(text)
        return VGroup(line, points, texts)

    def info_box(self, lines, color, width=3.05, height=1.25):
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
                    0.40 if index == 0 else 0.29
                )
                for index, line in enumerate(lines)
            ]
        ).arrange(DOWN, buff=0.07)
        text.move_to(box)
        return VGroup(box, text)
