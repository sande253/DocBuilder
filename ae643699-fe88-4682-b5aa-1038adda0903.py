import manim

class ChromosomeExplanation(manim.Scene):
    def construct(self):
        # --- 1. Introduction ---
        title = manim.Text("Chromosomes: The Blueprint of Life", font_size=48).to_edge(manim.UP)
        self.play(manim.Write(title))
        self.wait(1)

        intro_text = manim.Text("Chromosomes are thread-like structures found inside the nucleus of animal and plant cells.",
                          font_size=28, line_spacing=1.2).next_to(title, manim.DOWN, buff=0.8)
        intro_text.to_edge(manim.LEFT)
        self.play(manim.FadeIn(intro_text, shift=manim.UP))
        self.wait(2)
        self.play(manim.FadeOut(intro_text))

        # --- 2. DNA Double Helix ---
        self.play(title.animate.to_edge(manim.UP).scale(0.8))

        # Create the label VGroup for DNA Double Helix
        dna_label_text = manim.Text("1. DNA Double Helix", font_size=36)
        dna_label_rect = manim.Rectangle(width=dna_label_text.width + 0.5, height=dna_label_text.height + 0.3, color=manim.BLUE, fill_opacity=0.2, corner_radius=0.1)
        dna_label_text.move_to(dna_label_rect.get_center()) # Center text within its rectangle
        dna_label = manim.VGroup(dna_label_rect, dna_label_text).to_edge(manim.LEFT).shift(manim.UP*2.5)
        self.play(manim.Create(dna_label_rect), manim.Write(dna_label_text))

        # Create a simple DNA double helix using smooth VMobjects
        helix_points_1 = [
            [-2, 0, 0], [-1.5, 0.5, 0], [-1, 0, 0], [-0.5, -0.5, 0], [0, 0, 0],
            [0.5, 0.5, 0], [1, 0, 0], [1.5, -0.5, 0], [2, 0, 0]
        ]
        dna_strand1 = manim.VMobject().set_points_as_corners(helix_points_1).set_stroke(color=manim.BLUE, width=3)
        dna_strand1.make_smooth() # Smooth the points for a helix-like curve

        # Create the second strand by copying, flipping, and slightly shifting for visual effect
        dna_strand2 = dna_strand1.copy().set_stroke(color=manim.PURPLE, width=3)
        dna_strand2.flip(manim.UP) # Flip vertically
        dna_strand2.shift(manim.RIGHT * 0.1) # Small horizontal offset

        # Group the strands to form the DNA helix and position it
        current_structure = manim.VGroup(dna_strand1, dna_strand2).scale(1.5).move_to(manim.ORIGIN).shift(manim.LEFT*3)
        self.play(manim.Create(current_structure))

        dna_info_text = manim.Text("DNA carries genetic instructions.", font_size=24).next_to(current_structure, manim.RIGHT, buff=0.5)
        self.play(manim.Write(dna_info_text))
        self.wait(1.5)
        self.play(manim.FadeOut(dna_info_text))

        # --- 3. Histones and Nucleosomes ---
        # Create the label VGroup for Histones & Nucleosomes
        nucleosome_label_text = manim.Text("2. Histones & Nucleosomes", font_size=36)
        nucleosome_label_rect = manim.Rectangle(width=nucleosome_label_text.width + 0.5, height=nucleosome_label_text.height + 0.3, color=manim.GREEN, fill_opacity=0.2, corner_radius=0.1)
        nucleosome_label_text.move_to(nucleosome_label_rect.get_center()) # Center text within its rectangle
        nucleosome_label = manim.VGroup(nucleosome_label_rect, nucleosome_label_text).to_edge(manim.LEFT).shift(manim.UP*2.5)

        self.play(manim.Transform(dna_label, nucleosome_label)) # Transform the previous label to the current one

        # Represent histone proteins as a single circle for simplicity (changed from Sphere to Circle for 2D scene)
        histone_sphere = manim.Circle(radius=0.4, color=manim.ORANGE, fill_opacity=0.8)
        histone_text = manim.Text("Histone Proteins", font_size=24).next_to(histone_sphere, manim.DOWN, buff=0.3)
        histone_group = manim.VGroup(histone_sphere, histone_text).move_to(manim.RIGHT*2) # Position to the right of the DNA helix
        self.play(manim.FadeIn(histone_group, shift=manim.UP))
        self.wait(1)

        # Animate the DNA helix shrinking and moving towards the histone
        self.play(
            current_structure.animate.scale(0.3).next_to(histone_sphere, manim.LEFT, buff=0.5),
            manim.FadeOut(histone_text)
        )

        # Create a simplified visual representation of a nucleosome (DNA wrapped around a histone)
        nucleosome_histone = manim.Circle(radius=0.3, color=manim.ORANGE, fill_opacity=0.8)
        # Create a path that visually suggests DNA wrapping around the histone
        wrapped_dna_path = manim.VMobject().set_points_as_corners([
            nucleosome_histone.get_left() + manim.LEFT*0.5,
            nucleosome_histone.get_top() + manim.UP*0.2,
            nucleosome_histone.get_right() + manim.RIGHT*0.5,
            nucleosome_histone.get_bottom() + manim.DOWN*0.2,
            nucleosome_histone.get_left() + manim.LEFT*0.5
        ]).set_stroke(color=manim.BLUE_E, width=2)
        wrapped_dna_path.make_smooth()
        wrapped_dna_path.move_to(nucleosome_histone.get_center())
        
        # Combine the histone and the wrapped DNA representation into a single nucleosome unit
        nucleosome_unit_visual = manim.VGroup(nucleosome_histone, wrapped_dna_path)
        nucleosome_unit_visual.move_to(current_structure.get_center()) # Position it where the DNA helix ended up

        # Transform the straight DNA helix into the nucleosome visual
        self.play(
            manim.Transform(current_structure, nucleosome_unit_visual), # current_structure now becomes the first nucleosome
            manim.FadeOut(histone_group) # The original histone group is no longer needed
        )
        
        nucleosome_unit_label = manim.Text("Nucleosome", font_size=24).next_to(current_structure, manim.DOWN, buff=0.3)
        self.play(manim.FadeIn(nucleosome_unit_label))
        self.wait(1.5)

        # --- 4. Chromatin Fiber ---
        # Create the label VGroup for Chromatin Fiber
        chromatin_label_text = manim.Text("3. Chromatin Fiber", font_size=36)
        chromatin_label_rect = manim.Rectangle(width=chromatin_label_text.width + 0.5, height=chromatin_label_text.height + 0.3, color=manim.YELLOW, fill_opacity=0.2, corner_radius=0.1)
        chromatin_label_text.move_to(chromatin_label_rect.get_center()) # Center text within its rectangle
        chromatin_label = manim.VGroup(chromatin_label_rect, chromatin_label_text).to_edge(manim.LEFT).shift(manim.UP*2.5)

        self.play(manim.Transform(dna_label, chromatin_label), manim.FadeOut(nucleosome_unit_label))

        # Function to create a single nucleosome VGroup for reusability
        def create_single_nucleosome():
            histone = manim.Circle(radius=0.2, color=manim.ORANGE, fill_opacity=0.8)
            # Simplified wrapped DNA path for a smaller nucleosome
            wrapped_dna = manim.VMobject().set_points_as_corners([
                histone.get_left() + manim.LEFT*0.1,
                histone.get_top() + manim.UP*0.05,
                histone.get_right() + manim.RIGHT*0.1,
                histone.get_bottom() + manim.DOWN*0.05,
                histone.get_left() + manim.LEFT*0.1
            ]).set_stroke(color=manim.BLUE_E, width=1.5)
            wrapped_dna.make_smooth()
            wrapped_dna.move_to(histone.get_center())
            return manim.VGroup(histone, wrapped_dna)

        # Create multiple nucleosomes and arrange them to form a chain
        nucleosomes_array = manim.VGroup(*[create_single_nucleosome() for _ in range(5)])
        nucleosomes_array.arrange(manim.RIGHT, buff=0.5).scale(0.8).move_to(manim.ORIGIN).shift(manim.LEFT*2)
        
        # Transform the single nucleosome visual into the array of nucleosomes
        self.play(manim.Transform(current_structure, nucleosomes_array))
        self.wait(1)

        # Condense the array of nucleosomes into a chromatin fiber (a thicker, more condensed wavy line)
        chromatin_fiber = manim.VMobject().set_points_as_corners([
            [-3, 0, 0], [-2.5, 0.5, 0], [-2, 0, 0], [-1.5, -0.5, 0], [-1, 0, 0],
            [-0.5, 0.5, 0], [0, 0, 0], [0.5, -0.5, 0], [1, 0, 0],
            [1.5, 0.5, 0], [2, 0, 0], [2.5, -0.5, 0], [3, 0, 0]
        ]).set_stroke(color=manim.GREEN_B, width=8)
        chromatin_fiber.make_smooth()
        chromatin_fiber.move_to(manim.ORIGIN).shift(manim.RIGHT*2)

        chromatin_fiber_label = manim.Text("Chromatin Fiber", font_size=24).next_to(chromatin_fiber, manim.DOWN, buff=0.3)
        # Transform the array of nucleosomes into the chromatin fiber
        self.play(manim.Transform(current_structure, chromatin_fiber), manim.FadeIn(chromatin_fiber_label))
        self.wait(1.5)

        # --- 5. Chromosome Structure ---
        # Create the label VGroup for Chromosome Structure
        chromosome_label_text = manim.Text("4. Chromosome Structure", font_size=36)
        chromosome_label_rect = manim.Rectangle(width=chromosome_label_text.width + 0.5, height=chromosome_label_text.height + 0.3, color=manim.RED, fill_opacity=0.2, corner_radius=0.1)
        chromosome_label_text.move_to(chromosome_label_rect.get_center()) # Center text within its rectangle
        chromosome_label = manim.VGroup(chromosome_label_rect, chromosome_label_text).to_edge(manim.LEFT).shift(manim.UP*2.5)

        self.play(manim.Transform(dna_label, chromosome_label), manim.FadeOut(chromatin_fiber_label))

        # Condense chromatin fiber into a chromatid shape
        chromatid_shape = manim.Polygon(
            [-0.5, 2, 0], [-1, 1, 0], [-0.8, -1, 0], [-0.5, -2, 0],
            [0.5, -2, 0], [0.8, -1, 0], [1, 1, 0], [0.5, 2, 0],
            color=manim.RED_E, fill_opacity=0.8, stroke_width=2
        ).scale(0.8).shift(manim.LEFT*2)

        self.play(manim.Transform(current_structure, chromatid_shape))
        self.wait(1)

        # Create a full chromosome (two sister chromatids + centromere)
        sister_chromatid1 = chromatid_shape.copy().shift(manim.LEFT*0.7)
        sister_chromatid2 = chromatid_shape.copy().shift(manim.RIGHT*0.7)
        centromere = manim.Circle(radius=0.3, color=manim.GRAY, fill_opacity=0.8).move_to(manim.ORIGIN)

        chromosome_vgroup = manim.VGroup(sister_chromatid1, sister_chromatid2, centromere).scale(0.8).move_to(manim.ORIGIN).shift(manim.RIGHT*2)

        self.play(manim.Transform(current_structure, chromosome_vgroup))
        self.wait(1)

        # Labels for chromosome parts
        sister_chromatid_label_text = manim.Text("Sister Chromatids", font_size=20)
        sister_chromatid_label_rect = manim.Rectangle(width=sister_chromatid_label_text.width + 0.4, height=sister_chromatid_label_text.height + 0.2, color=manim.RED, fill_opacity=0.1, corner_radius=0.05)
        sister_chromatid_label_text.move_to(sister_chromatid_label_rect.get_center()) # Center text within its rectangle
        sister_chromatid_label = manim.VGroup(sister_chromatid_label_rect, sister_chromatid_label_text)
        sister_chromatid_label.next_to(sister_chromatid2, manim.RIGHT, buff=0.5)

        centromere_label_text = manim.Text("Centromere", font_size=20)
        centromere_label_rect = manim.Rectangle(width=centromere_label_text.width + 0.4, height=centromere_label_text.height + 0.2, color=manim.GRAY, fill_opacity=0.1, corner_radius=0.05)
        centromere_label_text.move_to(centromere_label_rect.get_center()) # Center text within its rectangle
        centromere_label = manim.VGroup(centromere_label_rect, centromere_label_text)
        centromere_label.next_to(centromere, manim.DOWN, buff=0.5)

        self.play(manim.FadeIn(sister_chromatid_label, shift=manim.UP), manim.FadeIn(centromere_label, shift=manim.UP))
        self.wait(2)

        # --- 6. Function and Importance ---
        # Create the label VGroup for Function & Importance
        function_label_text = manim.Text("5. Function & Importance", font_size=36)
        function_label_rect = manim.Rectangle(width=function_label_text.width + 0.5, height=function_label_text.height + 0.3, color=manim.TEAL, fill_opacity=0.2, corner_radius=0.1)
        function_label_text.move_to(function_label_rect.get_center()) # Center text within its rectangle
        function_label = manim.VGroup(function_label_rect, function_label_text).to_edge(manim.LEFT).shift(manim.UP*2.5)

        self.play(manim.Transform(dna_label, function_label), manim.FadeOut(sister_chromatid_label), manim.FadeOut(centromere_label))

        # Emphasize genetic information
        genetic_info_text = manim.Text("Chromosomes carry genes, which are segments of DNA.", font_size=28, line_spacing=1.2)
        genetic_info_text.next_to(current_structure, manim.LEFT, buff=1)
        self.play(manim.Write(genetic_info_text))
        self.play(manim.Indicate(current_structure, color=manim.YELLOW)) # Indicate the chromosome structure
        self.wait(1.5)

        heredity_text = manim.Text("These genes determine an organism's traits and are passed from parents to offspring.",
                             font_size=28, line_spacing=1.2).next_to(genetic_info_text, manim.DOWN, buff=0.8)
        self.play(manim.Write(heredity_text))
        self.wait(2)

        # Final summary
        summary_text = manim.Text("Chromosomes are essential for heredity and the proper functioning of cells.",
                            font_size=32, color=manim.GREEN_A).move_to(manim.ORIGIN)
        self.play(manim.FadeOut(current_structure), manim.FadeOut(genetic_info_text), manim.FadeOut(heredity_text), manim.FadeOut(dna_label), manim.FadeOut(title))
        self.play(manim.Write(summary_text))
        self.wait(3)

        self.play(manim.FadeOut(summary_text))
        self.wait(1)