from manim import *
import numpy as np


class CriptografiaDeIsogenias(Scene):
    def construct(self):
        title = self.top_text("Criptografía de isogenias").scale(1.04)
        self.play(Write(title), run_time=0.9)

        point_world = self.point_secret_scene().move_to(LEFT * 2.80 + UP * 0.25)
        curve_world = self.curve_secret_scene().move_to(RIGHT * 2.80 + UP * 0.25)
        bottom = self.bottom_text("Tras Shor, buscamos problemas de curvas que no sean solo Q = kP.")

        self.play(FadeIn(point_world), FadeIn(curve_world), Write(bottom), run_time=2.0)
        self.wait(5.0)

        narrative_1 = self.top_text("En isogenias, el secreto ya no es un punto: es un mapa entre curvas.")
        bottom_1 = self.bottom_text("isogenia = una función algebraica que transforma una curva en otra", color=GREEN, font="Cambria Math")
        phi_arrow = CurvedArrow(LEFT * 1.45 + UP * 0.72, RIGHT * 1.45 + UP * 0.72, color=GREEN, stroke_width=4, tip_length=0.18)
        phi_label = Text("φ", font="Cambria Math", color=GREEN).scale(0.62)
        phi_label.next_to(phi_arrow, UP, buff=0.08)
        self.play(
            Transform(title, narrative_1),
            ReplacementTransform(bottom, bottom_1),
            FadeOut(point_world),
            curve_world.animate.move_to(ORIGIN + UP * 0.15),
            Create(phi_arrow),
            Write(phi_label),
            run_time=1.4,
        )
        self.wait(5.5)

        e0 = self.curve_node("E₀", BLUE).move_to(LEFT * 3.25 + UP * 0.40)
        e1 = self.curve_node("E₁", GREEN).move_to(ORIGIN + UP * 0.40)
        e2 = self.curve_node("E₂", PURPLE).move_to(RIGHT * 3.25 + UP * 0.40)
        map_01 = Arrow(e0.get_right(), e1.get_left(), buff=0.20, color=GREEN, stroke_width=4)
        map_12 = Arrow(e1.get_right(), e2.get_left(), buff=0.20, color=GREEN, stroke_width=4)
        label_01 = Text("φ", font="Cambria Math", color=GREEN).scale(0.48).next_to(map_01, UP, buff=0.10)
        label_12 = Text("ψ", font="Cambria Math", color=GREEN).scale(0.48).next_to(map_12, UP, buff=0.10)

        narrative_2 = self.top_text("Una cadena de isogenias mueve la curva por una red de curvas vecinas.")
        bottom_2 = self.bottom_text("E₀  →  E₁  →  E₂: cambia la curva, no solo un punto dentro de ella", color=WHITE)
        self.play(
            Transform(title, narrative_2),
            ReplacementTransform(bottom_1, bottom_2),
            FadeOut(curve_world),
            FadeOut(phi_arrow),
            FadeOut(phi_label),
            FadeIn(e0),
            FadeIn(e1),
            FadeIn(e2),
            Create(map_01),
            Create(map_12),
            Write(label_01),
            Write(label_12),
            run_time=1.8,
        )
        self.wait(5.5)

        graph = self.isogeny_graph().move_to(ORIGIN + UP * 0.10)
        secret_path = self.path_on_graph(graph)
        start_label = Text("curva pública", font="Cambria", color=BLUE).scale(0.36).move_to(LEFT * 3.25 + UP * 2.05)
        end_label = Text("curva final", font="Cambria", color=PURPLE).scale(0.36).move_to(RIGHT * 3.15 + DOWN * 1.30)

        narrative_3 = self.top_text("Visto desde lejos, el problema es encontrar un camino oculto en un grafo enorme.")
        bottom_3 = self.bottom_text("clave privada = camino secreto entre curvas", color=GREEN, font="Cambria Math")
        self.play(
            Transform(title, narrative_3),
            ReplacementTransform(bottom_2, bottom_3),
            FadeOut(e0),
            FadeOut(e1),
            FadeOut(e2),
            FadeOut(map_01),
            FadeOut(map_12),
            FadeOut(label_01),
            FadeOut(label_12),
            FadeIn(graph),
            run_time=1.5,
        )
        self.play(Create(secret_path), Write(start_label), Write(end_label), run_time=1.4)
        self.wait(5.8)

        alice_path = self.path_card("Alice", "camino a", YELLOW).move_to(LEFT * 2.45 + UP * 0.55)
        bob_path = self.path_card("Bob", "camino b", RED).move_to(RIGHT * 2.45 + UP * 0.55)
        shared = self.curve_node("E_AB", GREEN).scale(0.92).move_to(DOWN * 1.05)
        alice_arrow = Arrow(alice_path.get_bottom(), shared.get_left() + UP * 0.10, buff=0.12, color=YELLOW, stroke_width=4)
        bob_arrow = Arrow(bob_path.get_bottom(), shared.get_right() + UP * 0.10, buff=0.12, color=RED, stroke_width=4)

        narrative_4 = self.top_text("La idea criptográfica: dos caminos secretos pueden llegar a una curva compartida.")
        bottom_4 = self.bottom_text("intercambian curvas públicas, pero no revelan sus caminos privados", color=WHITE)
        self.play(
            Transform(title, narrative_4),
            ReplacementTransform(bottom_3, bottom_4),
            FadeOut(graph),
            FadeOut(secret_path),
            FadeOut(start_label),
            FadeOut(end_label),
            FadeIn(alice_path),
            FadeIn(bob_path),
            Create(alice_arrow),
            Create(bob_arrow),
            FadeIn(shared),
            run_time=1.6,
        )
        self.play(Indicate(shared, color=GREEN, scale_factor=1.05), run_time=1.0)
        self.wait(5.8)

        post_quantum = self.info_box(["motivación", "resistir a Shor", "con otro tipo de problema"], GREEN, width=3.35, height=1.35).move_to(LEFT * 2.35 + UP * 0.15)
        caution = self.info_box(["pero cuidado", "familias concretas", "sí pueden caer"], RED, width=3.05, height=1.35).move_to(RIGHT * 2.50 + UP * 0.15)
        narrative_5 = self.top_text("Las isogenias fueron una vía post-cuántica prometedora, pero delicada.")
        bottom_5 = self.bottom_text("el diseño importa: no basta con cambiar de problema matemático", color=RED, font="Cambria Math")
        self.play(
            Transform(title, narrative_5),
            ReplacementTransform(bottom_4, bottom_5),
            FadeOut(alice_path),
            FadeOut(bob_path),
            FadeOut(alice_arrow),
            FadeOut(bob_arrow),
            FadeOut(shared),
            FadeIn(post_quantum),
            FadeIn(caution),
            run_time=1.4,
        )
        self.wait(5.8)

        final_graph = self.isogeny_graph(compact=True).move_to(ORIGIN + UP * 0.15)
        final_bottom = self.bottom_text("siguiente paso: ver el grafo de curvas donde viven esos caminos", color=GREEN, font="Cambria Math")
        narrative_6 = self.top_text("Para entenderlas, en el siguiente video miramos el grafo de isogenias.")
        self.play(
            Transform(title, narrative_6),
            ReplacementTransform(bottom_5, final_bottom),
            FadeOut(post_quantum),
            FadeOut(caution),
            FadeIn(final_graph),
            run_time=1.2,
        )
        self.play(Indicate(final_graph, color=GREEN, scale_factor=1.02), run_time=1.0)
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

    def point_secret_scene(self):
        axes = Axes(
            x_range=[-2.2, 2.2, 1],
            y_range=[-1.7, 1.9, 1],
            x_length=3.2,
            y_length=2.55,
            axis_config={"include_tip": False, "stroke_color": GRAY},
        )
        curve = axes.plot_implicit_curve(lambda x, y: y**2 - (x**3 - x + 0.65), color=BLUE, stroke_width=3)
        p = Dot(axes.c2p(-0.85, self.curve_y(-0.85)), color=YELLOW, radius=0.065)
        q = Dot(axes.c2p(0.70, self.curve_y(0.70)), color=RED, radius=0.065)
        arrow = CurvedArrow(p.get_center(), q.get_center(), angle=-TAU / 5, color=GREEN, stroke_width=3, tip_length=0.14)
        label = Text("secreto: k", font="Cambria Math", color=YELLOW).scale(0.36).next_to(axes, DOWN, buff=0.12)
        return VGroup(axes, curve, p, q, arrow, label)

    def curve_secret_scene(self):
        left = self.curve_node("E₀", BLUE).scale(0.72).move_to(LEFT * 0.95)
        right = self.curve_node("E₁", GREEN).scale(0.72).move_to(RIGHT * 0.95)
        arrow = Arrow(left.get_right(), right.get_left(), buff=0.15, color=GREEN, stroke_width=4)
        label = Text("secreto: φ", font="Cambria Math", color=GREEN).scale(0.36).next_to(VGroup(left, right, arrow), DOWN, buff=0.12)
        return VGroup(left, right, arrow, label)

    def curve_node(self, label, color):
        axes = Axes(
            x_range=[-1.7, 1.7, 1],
            y_range=[-1.35, 1.45, 1],
            x_length=1.85,
            y_length=1.42,
            axis_config={"include_tip": False, "stroke_color": GRAY, "stroke_width": 1.5},
        )
        curve = axes.plot_implicit_curve(lambda x, y: y**2 - (x**3 - x + 0.65), color=color, stroke_width=2.5)
        text = Text(label, font="Cambria Math", color=color).scale(0.38).next_to(axes, DOWN, buff=0.08)
        return VGroup(axes, curve, text)

    def curve_y(self, x):
        return np.sqrt(max(0, x**3 - x + 0.65))

    def isogeny_graph(self, compact=False):
        points = [
            LEFT * 3.25 + UP * 1.20,
            LEFT * 1.60 + UP * 1.55,
            ORIGIN + UP * 1.00,
            RIGHT * 1.55 + UP * 1.45,
            RIGHT * 3.15 + UP * 0.65,
            LEFT * 2.55 + DOWN * 0.35,
            LEFT * 0.90 + DOWN * 0.05,
            RIGHT * 0.80 + DOWN * 0.50,
            RIGHT * 2.55 + DOWN * 0.95,
            LEFT * 0.15 + DOWN * 1.55,
        ]
        if compact:
            points = [p * 0.82 for p in points]
        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 2), (2, 7), (7, 8), (6, 9), (9, 7)]
        lines = VGroup(*[Line(points[i], points[j], color=GRAY, stroke_width=2, stroke_opacity=0.50) for i, j in edges])
        dots = VGroup()
        for index, point in enumerate(points):
            color = BLUE if index == 0 else (PURPLE if index == 8 else WHITE)
            dots.add(Dot(point, color=color, radius=0.065))
        return VGroup(lines, dots)

    def path_on_graph(self, graph):
        dots = graph[1]
        indices = [0, 1, 2, 7, 8]
        path = VMobject(color=GREEN, stroke_width=5).set_points_as_corners([dots[i].get_center() for i in indices])
        return path

    def path_card(self, name, secret, color):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=2.20,
            height=1.05,
            color=color,
            fill_color="#151515",
            fill_opacity=0.92,
        )
        text = VGroup(
            Text(name, font="Cambria", color=color).scale(0.42),
            Text(secret, font="Cambria Math", color=WHITE).scale(0.34),
        ).arrange(DOWN, buff=0.10)
        text.move_to(box)
        return VGroup(box, text)

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
