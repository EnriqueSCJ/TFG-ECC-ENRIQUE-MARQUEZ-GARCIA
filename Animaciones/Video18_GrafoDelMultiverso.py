from manim import *
import numpy as np


class GrafoDelMultiverso(Scene):
    def construct(self):
        title = self.top_text("Grafo de isogenias").scale(1.04)
        self.play(Write(title), run_time=0.9)

        curve = self.curve_node("E", BLUE, show_axes=True).scale(1.25).move_to(ORIGIN + UP * 0.35)
        bottom = self.bottom_text("Ahora una curva elíptica completa se resume como un nodo.")
        self.play(FadeIn(curve), Write(bottom), run_time=1.7)
        self.wait(4.5)

        node = Dot(ORIGIN + UP * 0.35, color=BLUE, radius=0.095)
        node_label = Text("E", font="Cambria Math", color=BLUE).scale(0.46).next_to(node, DOWN, buff=0.12)
        narrative_1 = self.top_text("Cada nodo representa una curva; cada arista, una isogenia posible.")
        bottom_1 = self.bottom_text("curva  →  nodo        isogenia  →  conexión", color=GREEN, font="Cambria Math")
        self.play(Transform(title, narrative_1), ReplacementTransform(bottom, bottom_1), ReplacementTransform(curve, VGroup(node, node_label)), run_time=1.3)
        self.wait(4.8)

        local_graph = self.local_graph().move_to(ORIGIN + UP * 0.20)
        phi_labels = self.local_phi_labels()
        narrative_2 = self.top_text("Desde una curva hay varias isogenias: varios caminos posibles.")
        bottom_2 = self.bottom_text("el grado de la isogenia decide qué vecinos están conectados", color=WHITE)
        self.play(Transform(title, narrative_2), ReplacementTransform(bottom_1, bottom_2), ReplacementTransform(VGroup(node, node_label), local_graph), run_time=1.4)
        self.play(FadeIn(phi_labels), Indicate(local_graph, color=GREEN, scale_factor=1.02), run_time=1.0)
        self.wait(5.0)

        big_graph = self.big_graph().move_to(ORIGIN + UP * 0.05)
        narrative_3 = self.top_text("El grafo supersingular contiene muchísimas curvas conectadas por isogenias.")
        bottom_3 = self.bottom_text("no buscamos un punto en una curva, sino una ruta dentro de una red", color=GREEN, font="Cambria Math")
        self.play(
            Transform(title, narrative_3),
            ReplacementTransform(bottom_2, bottom_3),
            FadeOut(phi_labels),
            ReplacementTransform(local_graph, big_graph),
            run_time=1.7,
        )
        self.wait(5.0)

        start_dot = big_graph[1][0]
        end_dot = big_graph[1][13]
        path_indices = [0, 5, 6, 7, 8, 13]
        path = self.secret_path(big_graph, path_indices)
        walker = Dot(start_dot.get_center(), color=YELLOW, radius=0.075).set_z_index(5)
        start_label = self.label_box("inicio público", BLUE).move_to(LEFT * 3.20 + UP * 2.25)
        end_label = self.label_box("curva final", PURPLE).move_to(RIGHT * 3.05 + DOWN * 1.95)
        start_arrow = Arrow(start_label.get_bottom(), start_dot.get_center(), buff=0.10, color=BLUE, stroke_width=3)
        end_arrow = Arrow(end_label.get_top(), end_dot.get_center(), buff=0.10, color=PURPLE, stroke_width=3)

        narrative_4 = self.top_text("La clave privada puede verse como una ruta secreta entre dos curvas públicas.")
        bottom_4 = self.bottom_text("quien conoce el camino puede reproducirlo; quien solo ve los extremos debe reconstruirlo", color=WHITE)
        self.play(
            Transform(title, narrative_4),
            ReplacementTransform(bottom_3, bottom_4),
            FadeIn(walker),
            FadeIn(start_label),
            FadeIn(end_label),
            Create(start_arrow),
            Create(end_arrow),
            run_time=1.2,
        )
        self.play(Create(path), run_time=0.9)
        for start, end in zip(path_indices, path_indices[1:]):
            edge_path = Line(big_graph[1][start].get_center(), big_graph[1][end].get_center())
            self.play(MoveAlongPath(walker, edge_path), run_time=0.45, rate_func=smooth)
        self.wait(5.5)

        maze_box = self.info_box(["problema difícil", "encontrar camino", "entre curvas"], RED).move_to(LEFT * 2.65 + UP * 0.20)
        public_box = self.info_box(["datos públicos", "curva inicial", "curva final"], BLUE).move_to(RIGHT * 2.65 + UP * 0.20)
        narrative_5 = self.top_text("La seguridad pretendida: el grafo es público, pero el camino concreto queda oculto.")
        bottom_5 = self.bottom_text("mucha estructura visible, pero demasiados caminos posibles", color=RED, font="Cambria Math")
        self.play(
            Transform(title, narrative_5),
            ReplacementTransform(bottom_4, bottom_5),
            FadeOut(path),
            FadeOut(walker),
            FadeOut(start_label),
            FadeOut(end_label),
            FadeOut(start_arrow),
            FadeOut(end_arrow),
            big_graph.animate.set_opacity(0.28),
            FadeIn(maze_box),
            FadeIn(public_box),
            run_time=1.4,
        )
        self.wait(5.5)

        final_path = self.secret_path(big_graph, path_indices, color=GREEN)
        final_bottom = self.bottom_text("este es el escenario donde nacen SIDH y sus ataques posteriores", color=GREEN, font="Cambria Math")
        narrative_6 = self.top_text("En el último video veremos qué salió mal en una familia concreta: SIDH.")
        self.play(
            Transform(title, narrative_6),
            ReplacementTransform(bottom_5, final_bottom),
            FadeOut(maze_box),
            FadeOut(public_box),
            big_graph.animate.set_opacity(1.0),
            Create(final_path),
            run_time=1.4,
        )
        self.play(Indicate(final_path, color=GREEN, scale_factor=1.02), run_time=1.0)
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

    def curve_node(self, label, color, show_axes=False):
        axes = Axes(
            x_range=[-1.8, 1.8, 1],
            y_range=[-1.4, 1.5, 1],
            x_length=2.0,
            y_length=1.55,
            axis_config={"include_tip": False, "stroke_color": GRAY, "stroke_width": 1.5},
        )
        curve = axes.plot_implicit_curve(lambda x, y: y**2 - (x**3 - x + 0.65), color=color, stroke_width=3)
        text = Text(label, font="Cambria Math", color=color).scale(0.42).next_to(axes, DOWN, buff=0.08)
        if show_axes:
            return VGroup(axes, curve, text)
        return VGroup(curve, text)

    def local_graph(self):
        center = Dot(ORIGIN, color=BLUE, radius=0.085)
        neighbors = VGroup(
            Dot(LEFT * 1.35 + UP * 0.75, color=WHITE, radius=0.070),
            Dot(RIGHT * 1.45 + UP * 0.45, color=WHITE, radius=0.070),
            Dot(DOWN * 1.10, color=WHITE, radius=0.070),
        )
        edges = VGroup(*[Line(center.get_center(), dot.get_center(), color=GREEN, stroke_width=3) for dot in neighbors])
        label = Text("E", font="Cambria Math", color=BLUE).scale(0.38).next_to(center, RIGHT, buff=0.16).shift(DOWN * 0.05)
        return VGroup(edges, VGroup(center, neighbors), label)

    def local_phi_labels(self):
        return VGroup(
            Text("φ₁", font="Cambria Math", color=GREEN).scale(0.34).move_to(LEFT * 0.82 + UP * 1.06),
            Text("φ₂", font="Cambria Math", color=GREEN).scale(0.34).move_to(RIGHT * 0.95 + UP * 0.86),
            Text("φ₃", font="Cambria Math", color=GREEN).scale(0.34).move_to(RIGHT * 0.32 + DOWN * 0.67),
        )

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
            width=1.55,
            height=0.50,
            color=color,
            fill_color="#151515",
            fill_opacity=0.92,
        )
        label = Text(text, font="Cambria", color=color).scale(0.27)
        label.move_to(box)
        return VGroup(box, label)

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
