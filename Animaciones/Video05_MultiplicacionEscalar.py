from manim import *


class MultiplicacionEscalar(Scene):
    def construct(self):
        p = 17
        a = 2
        b = 2
        base = (5, 1)

        title = Text("Multiplicación escalar en una curva elíptica", font="Cambria").scale(0.46).to_edge(UP)
        self.play(Write(title))

        field = self.make_field_grid(p)
        cloud = self.make_solution_cloud(p, a, b)
        formula = Text("y² ≡ x³ + 2x + 2   (mod 17)", font="Cambria Math", color=WHITE).scale(0.58)
        formula.move_to(DOWN * 3.45)

        self.play(Create(field), LaggedStart(*[GrowFromCenter(dot) for dot in cloud], lag_ratio=0.02), Write(formula), run_time=2.0)

        narrative_1 = Text(
            "En un campo finito, la curva es una lista discreta de puntos.",
            font="Cambria",
        ).scale(0.45).to_edge(UP)
        self.play(Transform(title, narrative_1))
        self.wait(1.4)

        base_obj = self.point_with_label(base, p, "P", YELLOW, UP + LEFT)
        self.play(FadeIn(base_obj), Flash(base_obj[0], color=YELLOW, flash_radius=0.45), run_time=0.8)

        narrative_2 = Text(
            "Multiplicar por k significa sumar el mismo punto P consigo mismo k veces.",
            font="Cambria",
        ).scale(0.41).to_edge(UP)
        self.play(Transform(title, narrative_2))
        self.wait(1.0)

        definition = Text("kP = P + P + ... + P", font="Cambria Math", color=WHITE).scale(0.52)
        definition.move_to(DOWN * 2.9)
        self.play(Write(definition), run_time=0.9)
        self.wait(1.0)

        doubles = [(1, base), (2, self.ec_mul(2, base, p, a)), (4, self.ec_mul(4, base, p, a)), (8, self.ec_mul(8, base, p, a))]
        mover = Dot(self.field_to_point(*base, p), color=YELLOW, radius=0.09).set_z_index(5)
        mover_label = Text("P", font="Cambria Math", slant=ITALIC, color=YELLOW).scale(0.36)
        mover_label.next_to(mover, UP + LEFT, buff=0.08)
        mover_group = VGroup(mover, mover_label)
        self.add(mover_group)
        self.play(FadeOut(base_obj), run_time=0.2)

        step_text = Text("P", font="Cambria Math", color=YELLOW).scale(0.5).move_to(DOWN * 2.9)
        self.play(ReplacementTransform(definition, step_text), run_time=0.7)

        visited = VGroup()
        previous = base
        for value, point in doubles[1:]:
            label = f"{value}P"
            narrative = Text(
                f"Doblar el punto nos lleva de {value // 2}P a {label}.",
                font="Cambria",
            ).scale(0.45).to_edge(UP)
            next_step_text = Text(label, font="Cambria Math", color=YELLOW).scale(0.5).move_to(DOWN * 2.9)
            arrow = Arrow(
                self.field_to_point(*previous, p),
                self.field_to_point(*point, p),
                buff=0.13,
                color=GREEN,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.04,
            )
            self.play(Transform(title, narrative))
            self.wait(0.45)
            self.play(Create(arrow), run_time=0.55)
            self.play(
                mover.animate.move_to(self.field_to_point(*point, p)),
                ReplacementTransform(step_text, next_step_text),
                run_time=0.9,
                rate_func=smooth,
            )
            mover_label.become(
                Text(label, font="Cambria Math", slant=ITALIC, color=YELLOW)
                .scale(0.36)
                .next_to(mover, UP + LEFT, buff=0.08)
            )
            point_tag = self.point_with_label(point, p, label, YELLOW, UP + LEFT, scale=0.34)
            visited.add(point_tag)
            self.play(FadeIn(point_tag[1]), FadeOut(arrow), run_time=0.35)
            previous = point
            step_text = next_step_text

        narrative_6 = Text(
            "Con esos doblados calculamos potencias de dos: P, 2P, 4P, 8P.",
            font="Cambria",
        ).scale(0.42).to_edge(UP)
        doubling_summary = Text("P → 2P → 4P → 8P", font="Cambria Math", color=YELLOW).scale(0.48)
        doubling_summary.move_to(DOWN * 2.9)
        self.play(Transform(title, narrative_6), ReplacementTransform(step_text, doubling_summary), run_time=0.9)
        self.wait(1.5)

        narrative_7 = Text(
            "Por ejemplo, si queremos calcular 13P, usamos la escritura binaria: 13 = 8 + 4 + 1.",
            font="Cambria",
        ).scale(0.38).to_edge(UP)
        binary_formula = Text("13P = 8P + 4P + P", font="Cambria Math", color=WHITE).scale(0.54)
        binary_formula.move_to(DOWN * 2.9)
        self.play(
            Transform(title, narrative_7),
            ReplacementTransform(doubling_summary, binary_formula),
            FadeOut(formula),
            run_time=0.9,
        )
        self.wait(1.4)

        points = {
            "8P": self.ec_mul(8, base, p, a),
            "4P": self.ec_mul(4, base, p, a),
            "P": base,
            "12P": self.ec_mul(12, base, p, a),
            "13P": self.ec_mul(13, base, p, a),
        }

        selected = VGroup(
            self.selection_ring(points["8P"], p, GREEN),
            self.selection_ring(points["4P"], p, GREEN),
            self.point_with_label(points["P"], p, "P", GREEN, UP + LEFT, scale=0.34),
        )
        self.play(FadeIn(selected), run_time=0.8)
        self.play(Indicate(selected, color=GREEN, scale_factor=1.08), run_time=0.8)

        accumulator_text = Text("8P + 4P = 12P", font="Cambria Math", color=GREEN).scale(0.46)
        accumulator_text.move_to(DOWN * 3.38)
        arrow_1 = Arrow(
            self.field_to_point(*points["8P"], p),
            self.field_to_point(*points["12P"], p),
            buff=0.13,
            color=GREEN,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.04,
        )
        acc_obj = self.point_with_label(points["12P"], p, "12P", GREEN, LEFT, scale=0.32)
        self.play(Write(accumulator_text), Create(arrow_1), FadeIn(acc_obj), run_time=1.0)
        self.wait(1.0)

        target = points["13P"]
        target_obj = self.point_with_label(target, p, "13P", PURPLE, UP + RIGHT, scale=0.36)
        target_obj[1].shift(UP * 0.05 + RIGHT * 0.08)
        final_text = Text("12P + P = 13P", font="Cambria Math", color=PURPLE).scale(0.46)
        final_text.move_to(accumulator_text)
        arrow_2 = Arrow(
            self.field_to_point(*points["12P"], p),
            self.field_to_point(*target, p),
            buff=0.13,
            color=PURPLE,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.04,
        )
        self.play(ReplacementTransform(accumulator_text, final_text), Create(arrow_2), FadeIn(target_obj), run_time=1.0)
        self.play(Flash(target_obj[0], color=PURPLE, flash_radius=0.55), run_time=0.7)

        narrative_8 = Text(
            "El resultado parece irregular, pero cada salto está determinado por la misma regla de suma.",
            font="Cambria",
        ).scale(0.40).to_edge(UP)
        self.play(Transform(title, narrative_8))
        self.wait(1.1)
        self.play(Indicate(binary_formula, color=PURPLE, scale_factor=1.05), run_time=1.0)
        self.wait(3)

    def field_to_point(self, x, y, p):
        spacing = 0.29
        center = DOWN * 0.12
        return center + RIGHT * ((x - (p - 1) / 2) * spacing) + UP * ((y - (p - 1) / 2) * spacing)

    def make_field_grid(self, p):
        grid = VGroup()
        for x in range(p):
            for y in range(p):
                dot = Dot(self.field_to_point(x, y, p), color=GRAY, radius=0.014)
                dot.set_opacity(0.45)
                grid.add(dot)

        for value, direction in [(0, DOWN), (p - 1, DOWN)]:
            label = Text(str(value), font="Cambria Math", color=GRAY).scale(0.25)
            label.next_to(self.field_to_point(value, 0, p), direction, buff=0.1)
            grid.add(label)

        for value, direction in [(0, LEFT), (p - 1, LEFT)]:
            label = Text(str(value), font="Cambria Math", color=GRAY).scale(0.25)
            label.next_to(self.field_to_point(0, value, p), direction, buff=0.1)
            grid.add(label)

        return grid

    def make_solution_cloud(self, p, a, b):
        cloud = VGroup()
        for x in range(p):
            rhs = (x**3 + a * x + b) % p
            for y in range(p):
                if (y * y - rhs) % p == 0:
                    dot = Dot(self.field_to_point(x, y, p), color=BLUE, radius=0.055)
                    cloud.add(dot)
        return cloud

    def point_with_label(self, point, p, label, color, direction, scale=0.36):
        dot = Dot(self.field_to_point(*point, p), color=color, radius=0.09).set_z_index(4)
        text = Text(label, font="Cambria Math", slant=ITALIC, color=color).scale(scale)
        text.next_to(dot, direction, buff=0.08)
        return VGroup(dot, text)

    def selection_ring(self, point, p, color):
        ring = Circle(radius=0.13, color=color, stroke_width=3)
        ring.move_to(self.field_to_point(*point, p))
        ring.set_z_index(5)
        return ring

    def ec_add(self, point_1, point_2, p, a):
        if point_1 is None:
            return point_2
        if point_2 is None:
            return point_1

        x1, y1 = point_1
        x2, y2 = point_2
        if x1 == x2 and (y1 + y2) % p == 0:
            return None

        if point_1 == point_2:
            slope = ((3 * x1 * x1 + a) * pow(2 * y1, -1, p)) % p
        else:
            slope = ((y2 - y1) * pow(x2 - x1, -1, p)) % p

        x3 = (slope * slope - x1 - x2) % p
        y3 = (slope * (x1 - x3) - y1) % p
        return (x3, y3)

    def ec_mul(self, scalar, point, p, a):
        result = None
        addend = point
        while scalar:
            if scalar & 1:
                result = self.ec_add(result, addend, p, a)
            addend = self.ec_add(addend, addend, p, a)
            scalar >>= 1
        return result
