from manim import *
import numpy as np


class ProtocolosModernosECC(Scene):
    def construct(self):
        title = self.top_text("Protocolos modernos con ECC").scale(1.04)
        self.play(Write(title), run_time=0.9)

        overview = self.protocol_overview().scale(1.08).move_to(UP * 0.18)
        bottom = self.bottom_text("Las curvas ya no solo sirven para ECDH y ECDSA: también son bloques de protocolos nuevos.")
        self.play(FadeIn(overview), Write(bottom), run_time=1.8)
        self.wait(5.0)

        curve = self.curve_panel().scale(1.06).move_to(RIGHT * 1.95 + UP * 0.08)
        messages = VGroup(
            self.data_card("mensaje", "m", BLUE),
            self.data_card("dominio", "DST", PURPLE),
            self.data_card("hash", "H(m)", YELLOW),
        ).arrange(DOWN, buff=0.20).move_to(LEFT * 3.35 + UP * 0.20)
        h_arrow = Arrow(messages[1].get_right(), curve[3].get_left(), buff=0.15, color=YELLOW, stroke_width=4)
        narrative_1 = self.top_text("Hash-to-curve convierte datos normales en puntos válidos de una curva.")
        bottom_1 = self.bottom_text("antes de firmar o probar algo, el protocolo necesita un punto bien distribuido", color=YELLOW, font="Cambria Math")
        self.play(
            Transform(title, narrative_1),
            ReplacementTransform(bottom, bottom_1),
            FadeOut(overview),
            FadeIn(messages),
            FadeIn(curve),
            Create(h_arrow),
            run_time=1.6,
        )
        self.play(Flash(curve[3].get_center(), color=YELLOW, flash_radius=0.65), run_time=0.8)
        self.wait(5.6)

        bls = self.bls_signature_scene().scale(1.07).move_to(UP * 0.05)
        narrative_2 = self.top_text("BLS firma el punto H(m) multiplicándolo por una clave secreta.")
        bottom_2 = self.bottom_text("la firma σ = x H(m) es otro punto de la curva", color=GREEN, font="Cambria Math")
        self.play(
            Transform(title, narrative_2),
            ReplacementTransform(bottom_1, bottom_2),
            FadeOut(messages),
            FadeOut(curve),
            FadeOut(h_arrow),
            FadeIn(bls),
            run_time=1.5,
        )
        self.wait(5.6)

        pairing_check = self.pairing_check_scene().scale(1.07).move_to(UP * 0.05)
        narrative_3 = self.top_text("La verificación BLS usa pairings para comprobar la firma sin conocer x.")
        bottom_3 = self.bottom_text("e(σ, G) = e(H(m), X) conecta la firma, el mensaje y la clave pública", color=PURPLE, font="Cambria Math")
        self.play(
            Transform(title, narrative_3),
            ReplacementTransform(bottom_2, bottom_3),
            FadeOut(bls),
            FadeIn(pairing_check),
            run_time=1.5,
        )
        self.play(Indicate(pairing_check[1][2], color=GREEN, scale_factor=1.05), run_time=0.9)
        self.wait(5.8)

        aggregate = self.aggregate_scene().scale(1.06).move_to(UP * 0.10)
        narrative_4 = self.top_text("La gran ventaja de BLS: muchas firmas pueden agregarse en una sola.")
        bottom_4 = self.bottom_text("un bloque puede verificar cientos de participantes con una prueba compacta", color=GREEN, font="Cambria Math")
        self.play(
            Transform(title, narrative_4),
            ReplacementTransform(bottom_3, bottom_4),
            FadeOut(pairing_check),
            FadeIn(aggregate[0]),
            FadeIn(aggregate[1]),
            Create(aggregate[4][0]),
            run_time=1.5,
        )
        self.play(
            ReplacementTransform(aggregate[0].copy(), aggregate[2]),
            Create(aggregate[4][1]),
            FadeIn(aggregate[3]),
            Create(aggregate[4][2]),
            run_time=1.4,
        )
        self.play(Flash(aggregate[2].get_center(), color=GREEN, flash_radius=0.80), run_time=0.8)
        self.wait(5.8)

        vrf = self.vrf_scene().scale(1.04).move_to(UP * 0.10)
        narrative_5 = self.top_text("Otra pieza moderna es la VRF: azar verificable a partir de una clave.")
        bottom_5 = self.bottom_text("parece aleatorio, pero cualquiera puede comprobar que salió de la clave correcta", color=BLUE, font="Cambria Math")
        self.play(
            Transform(title, narrative_5),
            ReplacementTransform(bottom_4, bottom_5),
            FadeOut(aggregate),
            FadeIn(vrf),
            run_time=1.5,
        )
        self.wait(5.6)

        final = self.final_map().scale(1.08).move_to(UP * 0.10)
        narrative_6 = self.top_text("La ECC moderna combina curvas, hash, pairings y pruebas compactas.")
        final_bottom = self.bottom_text("la misma geometria sostiene firmas, consenso, identidad y verificabilidad", color=GREEN, font="Cambria Math")
        self.play(
            Transform(title, narrative_6),
            ReplacementTransform(bottom_5, final_bottom),
            FadeOut(vrf),
            FadeIn(final),
            run_time=1.4,
        )
        self.play(Indicate(final, color=GREEN, scale_factor=1.02), run_time=1.0)
        self.wait(6.0)

    def top_text(self, text, scale=0.60):
        mob = Text(text, font="Cambria").scale(scale)
        if mob.width > 12.4:
            mob.scale_to_fit_width(12.4)
        mob.to_edge(UP)
        return mob

    def bottom_text(self, text, color=WHITE, font="Cambria", scale=0.56):
        mob = Text(text, font=font, color=color).scale(scale)
        if mob.width > 11.8:
            mob.scale_to_fit_width(11.8)
        mob.move_to(DOWN * 3.05)
        return mob

    def protocol_overview(self):
        curve = self.mini_curve().move_to(LEFT * 3.65 + UP * 0.15)
        center = self.info_box(["ECC", "grupo de puntos", "estructura reutilizable"], GREEN, width=2.45, height=1.22).move_to(LEFT * 1.25 + UP * 0.15)
        apps = VGroup(
            self.small_card("BLS", "firmas cortas", BLUE),
            self.small_card("VRF", "azar verificable", PURPLE),
            self.small_card("zk", "pruebas compactas", YELLOW),
        ).arrange(DOWN, buff=0.20).move_to(RIGHT * 2.35 + UP * 0.15)
        arrows = VGroup(
            Arrow(curve.get_right(), center.get_left(), buff=0.16, color=GREEN, stroke_width=4),
            Arrow(center.get_right(), apps[0].get_left(), buff=0.16, color=BLUE, stroke_width=3),
            Arrow(center.get_right(), apps[1].get_left(), buff=0.16, color=PURPLE, stroke_width=3),
            Arrow(center.get_right(), apps[2].get_left(), buff=0.16, color=YELLOW, stroke_width=3),
        )
        return VGroup(curve, center, apps, arrows)

    def curve_panel(self):
        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-1.8, 1.8, 1],
            x_length=4.80,
            y_length=3.45,
            axis_config={"include_tip": False, "stroke_color": GRAY},
        )
        top = axes.plot(lambda x: 0.42 * np.sqrt(np.maximum(x + 2.0, 0)) * (2.35 - x) / 2.8, x_range=[-2.0, 2.25], color=BLUE, stroke_width=4)
        bottom = axes.plot(lambda x: -0.42 * np.sqrt(np.maximum(x + 2.0, 0)) * (2.35 - x) / 2.8, x_range=[-2.0, 2.25], color=BLUE, stroke_width=4)
        point_x = 0.75
        point_y = 0.42 * np.sqrt(point_x + 2.0) * (2.35 - point_x) / 2.8
        point = Dot(axes.c2p(point_x, point_y), color=YELLOW, radius=0.075)
        label = Text("H(m)", font="Cambria Math", color=YELLOW).scale(0.42).next_to(point, UP, buff=0.12)
        return VGroup(axes, top, bottom, point, label)

    def bls_signature_scene(self):
        message = self.data_card("mensaje", "m", BLUE).move_to(LEFT * 4.25 + UP * 0.45)
        hashed = self.data_card("punto", "H(m)", YELLOW).move_to(LEFT * 1.45 + UP * 0.45)
        secret = self.data_card("clave secreta", "x", RED).move_to(LEFT * 1.45 + DOWN * 1.05)
        signature = self.data_card("firma", "σ = xH(m)", GREEN, width=2.55).move_to(RIGHT * 2.30 + UP * 0.45)
        arrows = VGroup(
            Arrow(message.get_right(), hashed.get_left(), buff=0.16, color=YELLOW, stroke_width=4),
            Arrow(hashed.get_right(), signature.get_left(), buff=0.16, color=GREEN, stroke_width=4),
            Arrow(secret.get_top(), signature.get_bottom(), buff=0.16, color=RED, stroke_width=3),
        )
        product = self.caption_box("multiplicacion escalar", GREEN, width=2.25).move_to(RIGHT * 0.45 + DOWN * 0.82)
        return VGroup(message, hashed, secret, signature, arrows, product)

    def pairing_check_scene(self):
        left = self.check_card("e(σ, G)", GREEN)
        eq = Text("=", font="Cambria Math", color=WHITE).scale(0.78)
        right = self.check_card("e(H(m), X)", PURPLE)
        check = self.check_mark(GREEN).scale(0.85)
        formula = VGroup(left, eq, right, check).arrange(RIGHT, buff=0.22).move_to(UP * 0.65)

        lower = VGroup(
            self.data_card("firma", "σ", GREEN, width=1.80),
            self.data_card("generador", "G", BLUE, width=1.80),
            self.data_card("mensaje", "H(m)", YELLOW, width=1.80),
            self.data_card("clave pública", "X = xG", PURPLE, width=2.15),
        ).arrange(RIGHT, buff=0.18).move_to(DOWN * 0.95)
        return VGroup(lower, formula)

    def aggregate_scene(self):
        sigs = VGroup(
            self.signature_token("σ1", BLUE),
            self.signature_token("σ2", PURPLE),
            self.signature_token("σ3", YELLOW),
            self.signature_token("σ4", RED),
        ).arrange(DOWN, buff=0.20).move_to(LEFT * 3.65 + UP * 0.10)
        plus = Text("+", font="Cambria Math", color=WHITE).scale(0.68).move_to(LEFT * 1.65 + UP * 0.10)
        aggregate = self.data_card("firma agregada", "Σ", GREEN, width=2.35).move_to(RIGHT * 0.35 + UP * 0.10)
        verifier = self.info_box(["verificador", "comprueba el lote", "sin leer cada firma aparte"], BLUE, width=2.85, height=1.35).move_to(RIGHT * 3.35 + UP * 0.10)
        arrows = VGroup(
            Arrow(sigs.get_right(), plus.get_left(), buff=0.14, color=GRAY, stroke_width=3),
            Arrow(plus.get_right(), aggregate.get_left(), buff=0.14, color=GREEN, stroke_width=4),
            Arrow(aggregate.get_right(), verifier.get_left(), buff=0.16, color=GREEN, stroke_width=4),
        )
        return VGroup(sigs, plus, aggregate, verifier, arrows)

    def vrf_scene(self):
        left = VGroup(
            self.data_card("entrada pública", "α", BLUE, width=2.25),
            self.data_card("clave secreta", "x", RED, width=2.25),
        ).arrange(DOWN, buff=0.25).move_to(LEFT * 3.60 + UP * 0.15)
        engine = self.info_box(["VRF", "calcula y prueba", "sin revelar x"], PURPLE, width=2.40, height=1.35).move_to(LEFT * 0.55 + UP * 0.15)
        output = VGroup(
            self.data_card("salida", "y", GREEN, width=1.75),
            self.data_card("prueba", "π", YELLOW, width=1.75),
        ).arrange(DOWN, buff=0.24).move_to(RIGHT * 2.25 + UP * 0.15)
        public = self.info_box(["clave pública", "X = xG", "verifica y, π"], BLUE, width=2.30, height=1.22).move_to(RIGHT * 4.35 + UP * 0.15)
        arrows = VGroup(
            Arrow(left.get_right(), engine.get_left(), buff=0.16, color=PURPLE, stroke_width=4),
            Arrow(engine.get_right(), output.get_left(), buff=0.16, color=GREEN, stroke_width=4),
            Arrow(output.get_right(), public.get_left(), buff=0.16, color=BLUE, stroke_width=3),
        )
        return VGroup(left, engine, output, public, arrows)

    def final_map(self):
        center = self.info_box(["ECC moderna", "puntos + algebra", "interfaces seguras"], GREEN, width=2.65, height=1.34).move_to(ORIGIN)
        items = VGroup(
            self.small_card("hash-to-curve", "datos a puntos", YELLOW).move_to(LEFT * 3.65 + UP * 1.25),
            self.small_card("BLS", "firmas agregables", BLUE).move_to(RIGHT * 3.65 + UP * 1.25),
            self.small_card("VRF", "azar verificable", PURPLE).move_to(LEFT * 3.65 + DOWN * 1.05),
            self.small_card("zk/pairings", "pruebas cortas", GREEN).move_to(RIGHT * 3.65 + DOWN * 1.05),
        )
        arrows = VGroup(*[Arrow(center.get_center(), item.get_center(), buff=1.45, color=item[0].get_color(), stroke_width=3) for item in items])
        return VGroup(arrows, center, items)

    def mini_curve(self):
        axes = Axes(
            x_range=[-2.4, 2.4, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=2.25,
            y_length=1.70,
            axis_config={"include_tip": False, "stroke_color": GRAY},
        )
        top = axes.plot(lambda x: 0.36 * np.sqrt(np.maximum(x + 1.9, 0)) * (2.25 - x) / 2.6, x_range=[-1.9, 2.15], color=BLUE, stroke_width=3)
        bottom = axes.plot(lambda x: -0.36 * np.sqrt(np.maximum(x + 1.9, 0)) * (2.25 - x) / 2.6, x_range=[-1.9, 2.15], color=BLUE, stroke_width=3)
        point_x = 0.70
        point_y = 0.36 * np.sqrt(point_x + 1.9) * (2.25 - point_x) / 2.6
        dot = Dot(axes.c2p(point_x, point_y), color=YELLOW, radius=0.055)
        return VGroup(axes, top, bottom, dot)

    def data_card(self, title, value, color, width=2.05, height=0.86):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=width,
            height=height,
            color=color,
            fill_color="#151515",
            fill_opacity=0.92,
        )
        text = VGroup(
            Text(title, font="Cambria", color=WHITE).scale(0.29),
            Text(value, font="Cambria Math", color=color).scale(0.48),
        ).arrange(DOWN, buff=0.04)
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
                    0.42 if index == 0 else 0.30
                )
                for index, line in enumerate(lines)
            ]
        ).arrange(DOWN, buff=0.07)
        text.move_to(box)
        return VGroup(box, text)

    def small_card(self, title, subtitle, color):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=2.05,
            height=0.76,
            color=color,
            fill_color="#151515",
            fill_opacity=0.92,
        )
        text = VGroup(
            Text(title, font="Cambria Math", color=color).scale(0.34),
            Text(subtitle, font="Cambria", color=WHITE).scale(0.26),
        ).arrange(DOWN, buff=0.04)
        text.move_to(box)
        return VGroup(box, text)

    def signature_token(self, text, color):
        circle = Circle(radius=0.38, color=color, fill_color="#151515", fill_opacity=0.92, stroke_width=3)
        label = Text(text, font="Cambria Math", color=color).scale(0.30)
        if label.width > 0.60:
            label.scale_to_fit_width(0.60)
        label.move_to(circle)
        return VGroup(circle, label)

    def check_card(self, text, color):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=2.35,
            height=0.82,
            color=color,
            fill_color="#151515",
            fill_opacity=0.92,
        )
        label = Text(text, font="Cambria Math", color=color).scale(0.40)
        label.move_to(box)
        return VGroup(box, label)

    def caption_box(self, text, color, width=2.05):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=width,
            height=0.44,
            color=color,
            fill_color="#151515",
            fill_opacity=0.92,
        )
        label = Text(text, font="Cambria", color=WHITE).scale(0.30)
        if label.width > width - 0.24:
            label.scale_to_fit_width(width - 0.24)
        label.move_to(box)
        return VGroup(box, label)

    def check_mark(self, color=GREEN):
        mark = VMobject(color=color, stroke_width=7)
        mark.set_points_as_corners([LEFT * 0.24 + DOWN * 0.03, LEFT * 0.05 + DOWN * 0.22, RIGHT * 0.30 + UP * 0.22])
        return mark
