from manim import *


class AtaquePollardsRho(Scene):
    def construct(self):
        p = 17
        a = 2
        b = 2
        order = 19
        base = (5, 1)
        secret_k = 11
        target = self.ec_mul(secret_k, base, p, a)
        start_u = 1
        start_v = 1
        states = self.pollard_sequence(start_u, start_v, base, target, p, a, order)

        grid_offset = RIGHT * 2.05 + DOWN * 0.10
        panel_center = LEFT * 3.05 + DOWN * 0.05

        title = Text("Ataque Pollard rho", font="Cambria").scale(0.61).to_edge(UP)
        self.play(Write(title))

        grid = self.make_field_grid(p, grid_offset)
        cloud = self.make_solution_cloud(p, a, b, grid_offset)
        formula = Text("y² ≡ x³ + 2x + 2   (mod 17)", font="Cambria Math", color=WHITE).scale(0.58)
        formula.move_to(DOWN * 3.45)
        self.play(
            Create(grid),
            LaggedStart(*[GrowFromCenter(dot) for dot in cloud], lag_ratio=0.02),
            Write(formula),
            run_time=2.4,
        )

        narrative_1 = Text(
            "Pollard rho ataca el logaritmo discreto: dado Q = kP, busca k.",
            font="Cambria",
        ).scale(0.50).to_edge(UP)
        p_obj = self.point_with_label(base, p, "P", GREEN, DOWN + RIGHT, grid_offset, scale=0.40)
        q_obj = self.point_with_label(target, p, "Q", RED, UP + RIGHT, grid_offset, scale=0.40)
        q_formula = Text("Q = kP, con k desconocido", font="Cambria Math", color=WHITE).scale(0.58)
        q_formula.move_to(DOWN * 2.85)
        self.play(Transform(title, narrative_1), ReplacementTransform(formula, q_formula), run_time=1.2)
        self.play(FadeIn(p_obj), FadeIn(q_obj), run_time=1.2)
        self.play(Flash(q_obj[0], color=RED, flash_radius=0.45), run_time=0.9)
        self.wait(2.5)

        narrative_2 = Text(
            "El paseo guarda cada punto como una combinación X = uP + vQ.",
            font="Cambria",
        ).scale(0.52).to_edge(UP)
        state_box = RoundedRectangle(
            corner_radius=0.08,
            width=3.45,
            height=1.05,
            color=WHITE,
            fill_color="#161A24",
            fill_opacity=0.90,
        ).move_to(panel_center + UP * 0.62)
        state_label = Text("X = uP + vQ", font="Cambria Math", color=WHITE).scale(0.52).move_to(state_box)
        state_formula = Text("X = uP + vQ", font="Cambria Math", color=WHITE).scale(0.62).move_to(DOWN * 2.85)
        self.play(Transform(title, narrative_2), ReplacementTransform(q_formula, state_formula), run_time=1.2)
        self.play(FadeIn(state_box), Write(state_label), run_time=1.1)
        self.wait(2.3)

        narrative_3 = Text(
            "Una regla fija decide el siguiente salto: sumar P, sumar Q o doblar.",
            font="Cambria",
        ).scale(0.49).to_edge(UP)
        rules = VGroup(
            Text("zona 1  →  X + P", font="Cambria Math", color=GREEN).scale(0.36),
            Text("zona 2  →  X + Q", font="Cambria Math", color=RED).scale(0.36),
            Text("zona 3  →  2X", font="Cambria Math", color=YELLOW).scale(0.36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        rules.move_to(panel_center + DOWN * 0.65)
        rules_formula = Text("regla pseudoaleatoria", font="Cambria Math", color=YELLOW).scale(0.56).move_to(DOWN * 2.85)
        self.play(Transform(title, narrative_3), ReplacementTransform(state_formula, rules_formula), run_time=1.2)
        self.play(FadeIn(rules), run_time=1.0)
        self.wait(2.4)

        narrative_4 = Text(
            "Al moverse por un grupo finito, el paseo acaba repitiendo un punto.",
            font="Cambria",
        ).scale(0.51).to_edge(UP)
        walk_formula = Text("buscando una colisión...", font="Cambria Math", color=YELLOW).scale(0.58)
        walk_formula.move_to(DOWN * 2.85)
        self.play(Transform(title, narrative_4), ReplacementTransform(rules_formula, walk_formula), run_time=1.2)

        walker = Dot(self.field_to_point(*states[0]["point"], p, grid_offset), color=YELLOW, radius=0.095).set_z_index(6)
        walker_label = Text("X₀", font="Cambria Math", color=YELLOW).scale(0.36)
        walker_label.next_to(walker, UP + LEFT, buff=0.08)
        current_state = Text(
            self.state_text(0, states[0]),
            font="Cambria Math",
            color=YELLOW,
        ).scale(0.40).move_to(state_box)
        self.play(FadeOut(state_label), FadeIn(current_state), FadeIn(walker), FadeIn(walker_label), run_time=1.0)

        arrows = VGroup()
        state_text = current_state
        old_collision = states[-1]["collision_with"]
        for index in range(1, len(states)):
            previous = states[index - 1]["point"]
            current = states[index]["point"]
            arrow = Arrow(
                self.field_to_point(*previous, p, grid_offset),
                self.field_to_point(*current, p, grid_offset),
                buff=0.13,
                color=YELLOW,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.05,
            )
            arrow.set_opacity(0.78)
            next_state_text = Text(
                self.state_text(index, states[index]),
                font="Cambria Math",
                color=YELLOW,
            ).scale(0.40).move_to(state_box)
            next_label = Text(f"X{index}", font="Cambria Math", color=YELLOW).scale(0.36)
            next_label.next_to(walker, UP + LEFT, buff=0.08)
            self.play(Create(arrow), run_time=0.45)
            self.play(
                walker.animate.move_to(self.field_to_point(*current, p, grid_offset)),
                ReplacementTransform(state_text, next_state_text),
                run_time=0.72,
                rate_func=smooth,
            )
            walker_label.become(
                Text(f"X{index}", font="Cambria Math", color=YELLOW)
                .scale(0.36)
                .next_to(walker, UP + LEFT, buff=0.08)
            )
            arrows.add(arrow)
            state_text = next_state_text
            if index == old_collision:
                old_ring = Circle(radius=0.16, color=PURPLE, stroke_width=3).move_to(walker)
                old_ring.set_z_index(7)
                self.play(Create(old_ring), run_time=0.35)
            self.wait(0.15)

        collision_point = states[-1]["point"]
        collision_ring = Circle(radius=0.23, color=PURPLE, stroke_width=4).move_to(
            self.field_to_point(*collision_point, p, grid_offset)
        )
        collision_ring.set_z_index(8)
        self.play(Create(collision_ring), Flash(collision_ring, color=PURPLE, flash_radius=0.55), run_time=1.0)
        self.wait(1.0)

        narrative_5 = Text(
            "La colisión significa: dos combinaciones distintas llegaron al mismo punto.",
            font="Cambria",
        ).scale(0.49).to_edge(UP)
        collision_formula = Text("X₁ = X₉", font="Cambria Math", color=PURPLE).scale(0.62).move_to(DOWN * 2.85)
        self.play(Transform(title, narrative_5), ReplacementTransform(walk_formula, collision_formula), run_time=1.2)
        self.wait(2.4)

        old_state = states[old_collision]
        new_state = states[-1]
        detail_1 = Text(
            f"X₁ = {old_state['u']}P + {old_state['v']}Q",
            font="Cambria Math",
            color=PURPLE,
        ).scale(0.42)
        detail_2 = Text(
            f"X₉ = {new_state['u']}P + {new_state['v']}Q",
            font="Cambria Math",
            color=PURPLE,
        ).scale(0.42)
        details = VGroup(detail_1, detail_2).arrange(DOWN, buff=0.18).move_to(state_box)
        self.play(ReplacementTransform(state_text, details), run_time=1.0)
        self.wait(1.8)

        narrative_6 = Text(
            "Al despejar, aparece una ecuación que contiene el secreto k.",
            font="Cambria",
        ).scale(0.55).to_edge(UP)
        equation = Text("P + 2Q = 13P + 13Q", font="Cambria Math", color=WHITE).scale(0.56).move_to(DOWN * 2.85)
        self.play(Transform(title, narrative_6), ReplacementTransform(collision_formula, equation), run_time=1.2)
        self.wait(2.4)

        narrative_7 = Text(
            "Como Q = kP, esa relación permite recuperar k en el grupo.",
            font="Cambria",
        ).scale(0.53).to_edge(UP)
        solved = Text("7P = 11Q  →  k = 11", font="Cambria Math", color=GREEN).scale(0.62).move_to(DOWN * 2.85)
        self.play(Transform(title, narrative_7), ReplacementTransform(equation, solved), run_time=1.2)
        self.play(Indicate(solved, color=GREEN, scale_factor=1.05), Flash(q_obj[0], color=RED, flash_radius=0.45), run_time=1.2)
        self.wait(2.8)

        narrative_8 = Text(
            "En curvas reales el grupo es enorme: Pollard rho sigue siendo genérico, pero no barato.",
            font="Cambria",
        ).scale(0.44).to_edge(UP)
        final_text = Text("seguridad = grupos demasiado grandes para recorrer", font="Cambria Math", color=WHITE).scale(0.50)
        final_text.move_to(DOWN * 2.85)
        self.play(Transform(title, narrative_8), ReplacementTransform(solved, final_text), run_time=1.2)
        self.play(Indicate(arrows, color=YELLOW, scale_factor=1.02), run_time=1.0)
        self.wait(3.5)

    def state_text(self, index, state):
        return f"X{index} = {state['u']}P + {state['v']}Q"

    def pollard_sequence(self, start_u, start_v, base, target, p, a, order):
        point = self.ec_add(self.ec_mul(start_u, base, p, a), self.ec_mul(start_v, target, p, a), p, a)
        states = [{"point": point, "u": start_u, "v": start_v, "rule": "inicio"}]
        seen = {point: 0}

        for _ in range(1, 40):
            previous = states[-1]
            point, u, v, rule = self.pollard_step(previous["point"], previous["u"], previous["v"], base, target, p, a, order)
            state = {"point": point, "u": u, "v": v, "rule": rule}
            if point in seen:
                state["collision_with"] = seen[point]
                states.append(state)
                return states
            seen[point] = len(states)
            states.append(state)
        return states

    def pollard_step(self, point, u, v, base, target, p, a, order):
        selector = (point[0] + point[1]) % 3
        if selector == 0:
            return self.ec_add(point, point, p, a), (2 * u) % order, (2 * v) % order, "2X"
        if selector == 1:
            return self.ec_add(point, base, p, a), (u + 1) % order, v, "X+P"
        return self.ec_add(point, target, p, a), u, (v + 1) % order, "X+Q"

    def field_to_point(self, x, y, p, offset):
        spacing = 0.25
        return offset + RIGHT * ((x - (p - 1) / 2) * spacing) + UP * ((y - (p - 1) / 2) * spacing)

    def make_field_grid(self, p, offset):
        grid = VGroup()
        for x in range(p):
            for y in range(p):
                dot = Dot(self.field_to_point(x, y, p, offset), color=GRAY, radius=0.012)
                dot.set_opacity(0.42)
                grid.add(dot)

        for value in [0, p - 1]:
            x_label = Text(str(value), font="Cambria Math", color=GRAY).scale(0.22)
            x_label.next_to(self.field_to_point(value, 0, p, offset), DOWN, buff=0.08)
            y_label = Text(str(value), font="Cambria Math", color=GRAY).scale(0.22)
            y_label.next_to(self.field_to_point(0, value, p, offset), LEFT, buff=0.08)
            grid.add(x_label, y_label)

        return grid

    def make_solution_cloud(self, p, a, b, offset):
        cloud = VGroup()
        for x in range(p):
            rhs = (x**3 + a * x + b) % p
            for y in range(p):
                if (y * y - rhs) % p == 0:
                    cloud.add(Dot(self.field_to_point(x, y, p, offset), color=BLUE, radius=0.050))
        return cloud

    def point_with_label(self, point, p, label, color, direction, offset, scale=0.38):
        dot = Dot(self.field_to_point(*point, p, offset), color=color, radius=0.080).set_z_index(5)
        text = Text(label, font="Cambria Math", slant=ITALIC, color=color).scale(scale)
        text.next_to(dot, direction, buff=0.08)
        return VGroup(dot, text)

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
