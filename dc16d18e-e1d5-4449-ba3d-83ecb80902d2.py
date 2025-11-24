from manim import *

class ChromosomeExplanation(Scene):
    def construct(self):
        # --- 1. Introduction --- #
        title = Text("Chromosomes: The Blueprint of Life", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        intro_text = Text("Chromosomes are thread-like structures found inside the nucleus of animal and plant cells.",
                          font_size=28, line_spacing=1.2).next_to(title, DOWN, buff=0.8)
        intro_text.to_edge(LEFT)
        self.play(FadeIn(intro_text, shift=UP))
        self.wait(2)
        self.play(FadeOut(intro_text))

        # --- 2. DNA Double Helix --- #
        self.play(title.animate.to_edge(UP).scale(0.8))
        dna_label_text = Text("1. DNA Double Helix", font_size=36)
        dna_label_rect = Rectangle(width=dna_label_text.width + 0.5, height=dna_label_text.height + 0.3, color=BLUE, fill_opacity=0.2, corner_radius=0.1)
        dna_label = VGroup(dna_label_rect, dna_label_text).arrange(direction=RIGHT, buff=0).to_edge(LEFT).shift(UP*2.5)
        dna_label_text.move_to(dna_label_rect.get_center())
        self.play(Create(dna_label_rect), Write(dna_label_text))

        # Create a simple DNA double helix
        dna_strand1 = VMobject().set_points_as_corners([
            [-2, 0, 0], [-1.5, 0.5, 0], [-1, 0, 0], [-0.5, -0.5, 0], [0, 0, 0],
            [0.5, 0.5, 0], [1, 0, 0], [1.5, -0.5, 0], [2, 0, 0]
        ]).set_stroke(color=BLUE, width=3)
        dna_strand2 = VMobject().set_points_as_corners([
            [-2, 0, 0], [-1.5, -0.5, 0], [-1, 0, 0], [-0.5, 0.5, 0], [0, 0, 0],
            [0.5, -0.5, 0], [1, 0, 0], [1.5, 0.5, 0], [2, 0, 0]
        ]).set_stroke(color=PURPLE, width=3)
        dna_strand2.rotate(PI)
        dna_strand2.flip(UP)
        dna_strand2.move_to(dna_strand1.get_center())

        # Adjust points for a more helix-like appearance
        dna_strand1.set_points_smoothly(dna_strand1.get_points())
        dna_strand2.set_points_smoothly(dna_strand2.get_points())

        dna_helix = VGroup(dna_strand1, dna_strand2).scale(1.5).move_to(ORIGIN).shift(LEFT*3)
        self.play(Create(dna_helix))

        dna_info_text = Text("DNA carries genetic instructions.", font_size=24).next_to(dna_helix, RIGHT, buff=0.5)
        self.play(Write(dna_info_text))
        self.wait(1.5)
        self.play(FadeOut(dna_info_text))

        # --- 3. Histones and Nucleosomes --- #
        nucleosome_label_text = Text("2. Histones & Nucleosomes", font_size=36)
        nucleosome_label_rect = Rectangle(width=nucleosome_label_text.width + 0.5, height=nucleosome_label_text.height + 0.3, color=GREEN, fill_opacity=0.2, corner_radius=0.1)
        nucleosome_label = VGroup(nucleosome_label_rect, nucleosome_label_text).arrange(direction=RIGHT, buff=0).to_edge(LEFT).shift(UP*2.5)
        nucleosome_label_text.move_to(nucleosome_label_rect.get_center())

        self.play(Transform(dna_label, nucleosome_label))

        # Histones
        histone_circles = VGroup(*[Circle(radius=0.3, color=ORANGE, fill_opacity=0.8) for _ in range(4)])
        histone_circles.arrange(RIGHT, buff=0.2).next_to(dna_helix, RIGHT, buff=1)
        histone_text = Text("Histone Proteins", font_size=24).next_to(histone_circles, DOWN, buff=0.3)
        histone_group = VGroup(histone_circles, histone_text)
        self.play(FadeIn(histone_group, shift=UP))
        self.wait(1)

        # DNA wrapping around histones (Nucleosome)
        dna_helix_copy = dna_helix.copy().scale(0.5).next_to(histone_circles, LEFT, buff=0.1)
        dna_helix_copy.set_color(BLUE_E)
        self.play(dna_helix.animate.scale(0.5).move_to(histone_circles.get_center() + LEFT*0.5), FadeOut(histone_text))
        self.play(dna_helix.animate.wrap_around(histone_circles[0], radius=0.5, num_segments=20, run_time=2))
        self.play(dna_helix.animate.wrap_around(histone_circles[1], radius=0.5, num_segments=20, run_time=2))
        self.play(dna_helix.animate.wrap_around(histone_circles[2], radius=0.5, num_segments=20, run_time=2))
        self.play(dna_helix.animate.wrap_around(histone_circles[3], radius=0.5, num_segments=20, run_time=2))

        nucleosome_unit = VGroup(dna_helix, histone_circles)
        nucleosome_unit_label = Text("Nucleosome", font_size=24).next_to(nucleosome_unit, DOWN, buff=0.3)
        self.play(FadeIn(nucleosome_unit_label))
        self.wait(1.5)

        # --- 4. Chromatin Fiber --- #
        chromatin_label_text = Text("3. Chromatin Fiber", font_size=36)
        chromatin_label_rect = Rectangle(width=chromatin_label_text.width + 0.5, height=chromatin_label_text.height + 0.3, color=YELLOW, fill_opacity=0.2, corner_radius=0.1)
        chromatin_label = VGroup(chromatin_label_rect, chromatin_label_text).arrange(direction=RIGHT, buff=0).to_edge(LEFT).shift(UP*2.5)
        chromatin_label_text.move_to(chromatin_label_rect.get_center())

        self.play(Transform(dna_label, chromatin_label), FadeOut(nucleosome_unit_label))

        # Create multiple nucleosomes
        nucleosomes = VGroup()
        for i in range(5):
            histones_copy = VGroup(*[Circle(radius=0.2, color=ORANGE, fill_opacity=0.8) for _ in range(4)])
            histones_copy.arrange(RIGHT, buff=0.1)
            dna_segment = VMobject().set_points_as_corners([
                [-0.5, 0, 0], [-0.25, 0.25, 0], [0, 0, 0], [0.25, -0.25, 0], [0.5, 0, 0]
            ]).set_stroke(color=BLUE_E, width=2).scale(0.5)
            dna_segment.set_points_smoothly(dna_segment.get_points())
            nucleosome_i = VGroup(histones_copy, dna_segment.copy().wrap_around(histones_copy[0], radius=0.3, num_segments=10))
            nucleosome_i.add(dna_segment.copy().wrap_around(histones_copy[1], radius=0.3, num_segments=10))
            nucleosome_i.add(dna_segment.copy().wrap_around(histones_copy[2], radius=0.3, num_segments=10))
            nucleosome_i.add(dna_segment.copy().wrap_around(histones_copy[3], radius=0.3, num_segments=10))
            nucleosomes.add(nucleosome_i)

        nucleosomes.arrange(RIGHT, buff=0.5).scale(0.8).move_to(ORIGIN).shift(LEFT*2)
        self.play(Transform(nucleosome_unit, nucleosomes))
        self.wait(1)

        # Condense into chromatin fiber
        chromatin_fiber = VMobject().set_points_as_corners([
            [-3, 0, 0], [-2.5, 0.5, 0], [-2, 0, 0], [-1.5, -0.5, 0], [-1, 0, 0],
            [-0.5, 0.5, 0], [0, 0, 0], [0.5, -0.5, 0], [1, 0, 0],
            [1.5, 0.5, 0], [2, 0, 0], [2.5, -0.5, 0], [3, 0, 0]
        ]).set_stroke(color=GREEN_B, width=8)
        chromatin_fiber.set_points_smoothly(chromatin_fiber.get_points())
        chromatin_fiber.move_to(ORIGIN).shift(RIGHT*2)

        chromatin_fiber_label = Text("Chromatin Fiber", font_size=24).next_to(chromatin_fiber, DOWN, buff=0.3)
        self.play(Transform(nucleosome_unit, chromatin_fiber), FadeIn(chromatin_fiber_label))
        self.wait(1.5)

        # --- 5. Chromosome Structure --- #
        chromosome_label_text = Text("4. Chromosome Structure", font_size=36)
        chromosome_label_rect = Rectangle(width=chromosome_label_text.width + 0.5, height=chromosome_label_text.height + 0.3, color=RED, fill_opacity=0.2, corner_radius=0.1)
        chromosome_label = VGroup(chromosome_label_rect, chromosome_label_text).arrange(direction=RIGHT, buff=0).to_edge(LEFT).shift(UP*2.5)
        chromosome_label_text.move_to(chromosome_label_rect.get_center())

        self.play(Transform(dna_label, chromosome_label), FadeOut(chromatin_fiber_label))

        # Condense chromatin into a chromatid
        chromatid_shape = Polygon(
            [-0.5, 2, 0], [-1, 1, 0], [-0.8, -1, 0], [-0.5, -2, 0],
            [0.5, -2, 0], [0.8, -1, 0], [1, 1, 0], [0.5, 2, 0],
            color=RED_E, fill_opacity=0.8, stroke_width=2
        ).scale(0.8).shift(LEFT*2)

        self.play(Transform(nucleosome_unit, chromatid_shape))
        self.wait(1)

        # Create a full chromosome (two sister chromatids + centromere)
        sister_chromatid1 = chromatid_shape.copy().shift(LEFT*0.7)
        sister_chromatid2 = chromatid_shape.copy().shift(RIGHT*0.7)
        centromere = Circle(radius=0.3, color=GRAY, fill_opacity=0.8).move_to(ORIGIN)

        chromosome_vgroup = VGroup(sister_chromatid1, sister_chromatid2, centromere).scale(0.8).move_to(ORIGIN).shift(RIGHT*2)

        self.play(Transform(nucleosome_unit, chromosome_vgroup))
        self.wait(1)

        # Labels for chromosome parts
        sister_chromatid_label_text = Text("Sister Chromatids", font_size=20)
        sister_chromatid_label_rect = Rectangle(width=sister_chromatid_label_text.width + 0.4, height=sister_chromatid_label_text.height + 0.2, color=RED, fill_opacity=0.1, corner_radius=0.05)
        sister_chromatid_label = VGroup(sister_chromatid_label_rect, sister_chromatid_label_text)
        sister_chromatid_label_text.move_to(sister_chromatid_label_rect.get_center())
        sister_chromatid_label.next_to(sister_chromatid2, RIGHT, buff=0.5)

        centromere_label_text = Text("Centromere", font_size=20)
        centromere_label_rect = Rectangle(width=centromere_label_text.width + 0.4, height=centromere_label_text.height + 0.2, color=GRAY, fill_opacity=0.1, corner_radius=0.05)
        centromere_label = VGroup(centromere_label_rect, centromere_label_text)
        centromere_label_text.move_to(centromere_label_rect.get_center())
        centromere_label.next_to(centromere, DOWN, buff=0.5)

        self.play(FadeIn(sister_chromatid_label, shift=UP), FadeIn(centromere_label, shift=UP))
        self.wait(2)

        # --- 6. Function and Importance --- #
        function_label_text = Text("5. Function & Importance", font_size=36)
        function_label_rect = Rectangle(width=function_label_text.width + 0.5, height=function_label_text.height + 0.3, color=TEAL, fill_opacity=0.2, corner_radius=0.1)
        function_label = VGroup(function_label_rect, function_label_text).arrange(direction=RIGHT, buff=0).to_edge(LEFT).shift(UP*2.5)
        function_label_text.move_to(function_label_rect.get_center())

        self.play(Transform(dna_label, function_label), FadeOut(sister_chromatid_label), FadeOut(centromere_label))

        # Emphasize genetic information
        genetic_info_text = Text("Chromosomes carry genes, which are segments of DNA.", font_size=28, line_spacing=1.2)
        genetic_info_text.next_to(chromosome_vgroup, LEFT, buff=1)
        self.play(Write(genetic_info_text))
        self.play(Indicate(chromosome_vgroup, color=YELLOW))
        self.wait(1.5)

        heredity_text = Text("These genes determine an organism's traits and are passed from parents to offspring.",
                             font_size=28, line_spacing=1.2).next_to(genetic_info_text, DOWN, buff=0.8)
        self.play(Write(heredity_text))
        self.wait(2)

        # Final summary
        summary_text = Text("Chromosomes are essential for heredity and the proper functioning of cells.",
                            font_size=32, color=GREEN_A).move_to(ORIGIN)
        self.play(FadeOut(chromosome_vgroup), FadeOut(genetic_info_text), FadeOut(heredity_text), FadeOut(dna_label))
        self.play(Write(summary_text))
        self.wait(3)

        self.play(FadeOut(title), FadeOut(summary_text))
        self.wait(1)
