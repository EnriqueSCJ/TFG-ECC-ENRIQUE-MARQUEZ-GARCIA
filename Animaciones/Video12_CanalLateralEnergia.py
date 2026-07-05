from manim import *
import numpy as np


class CanalLateralEnergia(Scene):
    def construct(self):
        p = 17
        a = 2
        b = 2
        base = (5, 1)
        bits = [1, 0, 1, 1, 0, 1]
        walk = self.double_and_add_walk(bits, base, p, a)

        title = self.top_text("Canal lateral de energía").scale(1.02)
        self.play(Write(title), run_time=0.9)

        grid_offset = UP * 1.05
        grid = self.make_field_grid(p, grid_offset)
        cloud = self.make_solution_cloud(p, a, b, grid_offset)
        mover = self.point_with_label(base, p, "P", YELLOW, UP + RIGHT, grid_offset, scale=0.38)

        bottom = Text("La clave privada k controla una sucesión de operaciones sobre puntos.", font="Cambria").scale(0.46)
        bottom.move_to(DOWN * 3.35)
        self.play(
            Create(grid),
            LaggedStart(*[GrowFromCenter(dot) for dot in cloud], lag_ratio=0.02),
            FadeIn(mover),
            Write(bottom),
            run_time=2.0,
        )
        self.wait(1.5)

        narrative_1 = self.top_text("En doble-y-suma, cada bit decide si solo doblamos o también sumamos P.")
        rule = VGroup(
            Text("bit 0  →  doblar", font="Cambria Math", color=GREEN).scale(0.44),
            Text("bit 1  →  doblar + sumar", font="Cambria Math", color=RED).scale(0.44),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        rule_box = RoundedRectangle(
            corner_radius=0.08,
            width=3.20,
            height=1.20,
            color=WHITE,
            fill_color="#151515",
            fill_opacity=0.88,
        ).move_to(LEFT * 3.15 + UP * 1.15)
        rule.move_to(rule_box)
        bottom_1 = self.make_formula(["k", "=", "101101₂"], [PURPLE, WHITE, PURPLE], scale=0.60)
        self.play(Transform(title, narrative_1), ReplacementTransform(bottom, bottom_1), FadeIn(rule_box), FadeIn(rule), run_time=1.2)
        self.wait(2.4)

        trace_y = -2.42
        axis = Line(np.array([-4.55, trace_y, 0]), np.array([4.45, trace_y, 0]), color=GRAY, stroke_width=2)
        y_axis = Line(np.array([-4.35, trace_y - 0.20, 0]), np.array([-4.35, trace_y + 1.80, 0]), color=GRAY, stroke_width=2)
        energy_label = Text("energía", font="Cambria", color=WHITE).scale(0.32).rotate(PI / 2)
        energy_label.next_to(y_axis, LEFT, buff=0.15)
        time_label = Text("tiempo", font="Cambria", color=WHITE).scale(0.34)
        time_label.next_to(axis, RIGHT, buff=0.12)

        narrative_2 = self.top_text("El cálculo parece matemático, pero el chip deja una huella física.")
        bottom_2 = Text("medimos consumo eléctrico mientras avanza la multiplicación escalar", font="Cambria", color=WHITE).scale(0.46)
        bottom_2.move_to(DOWN * 3.35)
        self.play(
            Transform(title, narrative_2),
            ReplacementTransform(bottom_1, bottom_2),
            Create(axis),
            Create(y_axis),
            Write(energy_label),
            Write(time_label),
            FadeOut(rule_box),
            FadeOut(rule),
            run_time=1.2,
        )
        self.wait(1.2)

        path_points = [np.array([-4.25, trace_y, 0])]
        waveform = VMobject(color=GREEN, stroke_width=4).set_points_as_corners(path_points)
        self.add(waveform)
        current_point = mover
        labels = VGroup()
        x = -3.65

        for index, bit in enumerate(bits):
            step = walk[index]
            target = self.point_with_label(step["point"], p, f"X{index + 1}", YELLOW, UP + RIGHT, grid_offset, scale=0.30)
            operation_color = RED if bit == 1 else GREEN
            operation_label = Text(
                "doblar + sumar" if bit == 1 else "doblar",
                font="Cambria Math",
                color=operation_color,
            ).scale(0.30)
            operation_label.move_to(np.array([x, -0.52, 0]))

            height = 1.28 if bit == 1 else 0.66
            new_points = path_points + [
                np.array([x - 0.24, trace_y, 0]),
                np.array([x, trace_y + height, 0]),
                np.array([x + 0.24, trace_y, 0]),
            ]
            next_waveform = VMobject(color=GREEN, stroke_width=4).set_points_as_corners(new_points)
            peak_dot = Dot(np.array([x, trace_y + height, 0]), color=operation_color, radius=0.045)
            bit_label = Text(str(bit), font="Cambria Math", color=operation_color).scale(0.34)
            bit_label.next_to(peak_dot, UP, buff=0.08)

            self.play(ReplacementTransform(current_point, target), run_time=0.45)
            self.play(ReplacementTransform(waveform, next_waveform), FadeIn(peak_dot), Write(operation_label), Write(bit_label), run_time=0.45)
            self.wait(0.12)
            self.play(FadeOut(operation_label), run_time=0.16)

            labels.add(peak_dot, bit_label)
            waveform = next_waveform
            current_point = target
            path_points = new_points
            x += 1.20

        self.wait(1.0)

        narrative_3 = self.top_text("Los picos bajos y altos delatan qué operación se hizo en cada paso.")
        legend = VGroup(
            Text("pico bajo = bit 0", font="Cambria Math", color=GREEN).scale(0.40),
            Text("pico alto = bit 1", font="Cambria Math", color=RED).scale(0.40),
        ).arrange(RIGHT, buff=0.70)
        legend.move_to(DOWN * 0.28)
        legend_box = RoundedRectangle(
            corner_radius=0.08,
            width=5.05,
            height=0.62,
            color=WHITE,
            fill_color="#151515",
            fill_opacity=0.88,
        ).move_to(legend)
        bottom_3 = Text("la traza de energía contiene una copia visual de los bits", font="Cambria", color=WHITE).scale(0.48)
        bottom_3.move_to(DOWN * 3.35)
        self.play(Transform(title, narrative_3), ReplacementTransform(bottom_2, bottom_3), FadeIn(legend_box), FadeIn(legend), run_time=1.2)
        self.play(Indicate(labels, color=RED, scale_factor=1.04), run_time=1.0)
        self.wait(3.0)

        secret_bits = self.make_formula(
            ["1", "0", "1", "1", "0", "1"],
            [RED, GREEN, RED, RED, GREEN, RED],
            scale=0.72,
        )
        secret_bits.move_to(UP * 0.68)
        reveal = self.make_formula(["k", "=", "101101₂"], [PURPLE, WHITE, PURPLE], scale=0.70)
        reveal.move_to(UP * 0.08)

        narrative_4 = self.top_text("Así, una medición externa puede revelar bits de la clave privada.")
        bottom_4 = Text("canal lateral: no rompe la matemática, rompe la implementación", font="Cambria Math", color=RED).scale(0.52)
        bottom_4.move_to(DOWN * 3.35)
        self.play(
            Transform(title, narrative_4),
            ReplacementTransform(bottom_3, bottom_4),
            FadeOut(legend_box),
            FadeOut(legend),
            FadeOut(grid),
            FadeOut(cloud),
            FadeOut(current_point),
            run_time=1.2,
        )
        self.play(TransformFromCopy(labels, secret_bits), run_time=1.0)
        self.play(Write(reveal), Flash(reveal.get_center(), color=RED, flash_radius=0.85), run_time=1.0)
        self.wait(3.0)

        narrative_5 = self.top_text("La defensa es hacer que el consumo no dependa del bit secreto.")
        safe_points = [np.array([-4.25, trace_y, 0])]
        safe_labels = VGroup()
        safe_x = -3.65
        for bit in bits:
            safe_points.extend(
                [
                    np.array([safe_x - 0.24, trace_y, 0]),
                    np.array([safe_x, trace_y + 0.92, 0]),
                    np.array([safe_x + 0.24, trace_y, 0]),
                ]
            )
            bit_text = Text(f"bit {bit}", font="Cambria Math", color=WHITE).scale(0.25)
            bit_text.move_to(np.array([safe_x, trace_y - 0.34, 0]))
            work_text = Text("D+S", font="Cambria Math", color=GREEN).scale(0.25)
            work_text.next_to(bit_text, DOWN, buff=0.05)
            safe_labels.add(bit_text, work_text)
            safe_x += 1.20
        safe_waveform = VMobject(color=GREEN, stroke_width=4).set_points_as_corners(safe_points)
        defense_box = RoundedRectangle(
            corner_radius=0.08,
            width=5.80,
            height=0.92,
            color=GREEN,
            fill_color="#102013",
            fill_opacity=0.90,
        ).move_to(UP * 0.48)
        defense_text = Text("implementación en tiempo y patrón constantes", font="Cambria Math", color=GREEN).scale(0.39)
        defense_text.move_to(defense_box)
        final_bottom = Text("misma traza para 0 y para 1  →  menos filtración", font="Cambria Math", color=GREEN).scale(0.52)
        final_bottom.move_to(DOWN * 3.35)
        self.play(
            Transform(title, narrative_5),
            ReplacementTransform(bottom_4, final_bottom),
            FadeOut(secret_bits),
            FadeOut(reveal),
            FadeOut(labels),
            ReplacementTransform(waveform, safe_waveform),
            FadeIn(defense_box),
            Write(defense_text),
            FadeIn(safe_labels),
            run_time=1.2,
        )
        self.play(Indicate(defense_box, color=GREEN, scale_factor=1.04), run_time=1.0)
        self.wait(4.0)

    def top_text(self, text, scale=0.54):
        mob = Text(text, font="Cambria").scale(scale)
        if mob.width > 12.4:
            mob.scale_to_fit_width(12.4)
        mob.to_edge(UP)
        return mob

    def make_formula(self, parts, colors, scale=0.58):
        formula = VGroup(
            *[
                Text(
                    part,
                    font="Cambria Math",
                    slant=ITALIC if part not in ["=", "→"] else NORMAL,
                    color=color,
                )
                for part, color in zip(parts, colors)
            ]
        )
        formula.arrange(RIGHT, buff=0.14).scale(scale)
        formula.move_to(DOWN * 3.35)
        return formula

    def field_to_point(self, x, y, p, offset):
        spacing = 0.20
        return offset + RIGHT * ((x - (p - 1) / 2) * spacing) + UP * ((y - (p - 1) / 2) * spacing)

    def make_field_grid(self, p, offset):
        grid = VGroup()
        for x in range(p):
            for y in range(p):
                dot = Dot(self.field_to_point(x, y, p, offset), color=GRAY, radius=0.010)
                dot.set_opacity(0.38)
                grid.add(dot)

        for value in [0, p - 1]:
            x_label = Text(str(value), font="Cambria Math", color=GRAY).scale(0.20)
            x_label.next_to(self.field_to_point(value, 0, p, offset), DOWN, buff=0.07)
            y_label = Text(str(value), font="Cambria Math", color=GRAY).scale(0.20)
            y_label.next_to(self.field_to_point(0, value, p, offset), LEFT, buff=0.07)
            grid.add(x_label, y_label)

        return grid

    def make_solution_cloud(self, p, a, b, offset):
        cloud = VGroup()
        for x in range(p):
            rhs = (x**3 + a * x + b) % p
            for y in range(p):
                if (y * y - rhs) % p == 0:
                    cloud.add(Dot(self.field_to_point(x, y, p, offset), color=BLUE, radius=0.040))
        return cloud

    def point_with_label(self, point, p, label, color, direction, offset, scale=0.38):
        dot = Dot(self.field_to_point(*point, p, offset), color=color, radius=0.075).set_z_index(5)
        text = Text(label, font="Cambria Math", slant=ITALIC, color=color).scale(scale)
        text.next_to(dot, direction, buff=0.08)
        return VGroup(dot, text)

    def double_and_add_walk(self, bits, base, p, a):
        result = None
        walk = []
        for bit in bits:
            if result is not None:
                result = self.ec_add(result, result, p, a)
            if bit == 1:
                result = self.ec_add(result, base, p, a)
            walk.append({"bit": bit, "point": result or base})
        return walk

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
