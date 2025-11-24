import manim
from manim import *

class ChromosomeExplanation(Scene):
    def construct(self):
        # --- Colors --- 
        DNA_COLOR = BLUE_D
        HISTONE_COLOR = YELLOW_B
        CHROMATIN_COLOR = ORANGE_D
        CHROMOSOME_COLOR = PURPLE_D
        TEXT_COLOR = WHITE
        GENE_COLOR = YELLOW_E
        CENTROMERE_COLOR = RED_C

        # --- Title --- 
        title = Text("The Journey to a Chromosome", font_size=48, color=TEXT_COLOR).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # --- Part 1: DNA Double Helix --- 
        dna_label_text = Text("DNA Double Helix", font_size=30, color=TEXT_COLOR)
        
        # Simplified DNA helix representation with two wavy lines and connectors
        dna_strand1 = VMobject().set_points_as_corners([
            [-1, 0.5, 0], [-0.5, -0.5, 0], [0, 0.5, 0], [0.5, -0.5, 0], [1, 0.5, 0]
        ]).set_stroke(DNA_COLOR, 4)
        dna_strand2 = VMobject().set_points_as_corners([
            [-1, -0.5, 0], [-0.5, 0.5, 0], [0, -0.5, 0], [0.5, 0.5, 0], [1, -0.5, 0]
        ]).set_stroke(DNA_COLOR, 4)
        
        # Connecting bases (simplified as lines)
        dna_connectors = VGroup(*[
            Line(dna_strand1.get_point_from_proportion(i/4), dna_strand2.get_point_from_proportion(i/4), color=DNA_COLOR, stroke_width=2)
            for i in range(5)
        ])
        
        dna_helix_shape = VGroup(dna_strand1, dna_strand2, dna_connectors).scale(1.5).move_to(LEFT * 3 + DOWN * 1)
        # VGroup containing the shape and its centered text label
        dna_element = VGroup(dna_helix_shape, dna_label_text.next_to(dna_helix_shape, DOWN, buff=0.5))
        
        self.play(FadeIn(dna_element, shift=UP))
        self.wait(1.5)

        # --- Part 2: Histone Proteins and Nucleosome Formation --- 
        histone_label_text = Text("Histone Proteins", font_size=30, color=TEXT_COLOR)
        histone_shape = Circle(radius=0.4, color=HISTONE_COLOR, fill_opacity=0.8)
        # Arrange multiple histone shapes
        histone_group = VGroup(*[histone_shape.copy() for _ in range(4)]).arrange(RIGHT, buff=0.2).next_to(dna_element, RIGHT, buff=2)
        # VGroup containing the histone shapes and its centered text label
        histone_element = VGroup(histone_group, histone_label_text.next_to(histone_group, DOWN, buff=0.5))

        self.play(FadeIn(histone_element, shift=UP))
        self.wait(1)

        # Animate DNA wrapping around histones to form a nucleosome
        nucleosome_label_text = Text("Nucleosome", font_size=30, color=TEXT_COLOR)
        
        # Simplified nucleosome shape: DNA wrapped around a central histone group
        # Representing the wrapped DNA as arcs
        wrapped_dna_segment = Arc(radius=0.8, start_angle=PI/2, angle=-PI*1.5, color=DNA_COLOR, stroke_width=4)
        wrapped_dna_segment2 = Arc(radius=0.8, start_angle=PI/2 + PI, angle=-PI*1.5, color=DNA_COLOR, stroke_width=4)
        
        nucleosome_core = Circle(radius=0.6, color=HISTONE_COLOR, fill_opacity=0.8) # Represents the histone octamer
        nucleosome_shape = VGroup(nucleosome_core, wrapped_dna_segment, wrapped_dna_segment2).scale(1.2)
        
        # Position the nucleosome where the DNA and histones were
        target_nucleosome_pos = dna_element.get_center() + RIGHT * 2.5
        nucleosome_shape.move_to(target_nucleosome_pos)
        # VGroup containing the nucleosome shape and its centered text label
        nucleosome_element = VGroup(nucleosome_shape, nucleosome_label_text.next_to(nucleosome_shape, DOWN, buff=0.5))

        self.play(
            FadeOut(dna_element), # Fade out original DNA
            FadeOut(histone_element), # Fade out original histones
            FadeIn(nucleosome_element, shift=UP) # Fade in the new nucleosome element
        )
        self.wait(1.5)

        # --- Part 3: Chromatin Fiber Formation --- 
        chromatin_label_text = Text("Chromatin Fiber", font_size=30, color=TEXT_COLOR)
        
        # Create multiple nucleosomes to show coiling
        nucleosomes_for_fiber = VGroup(*[nucleosome_shape.copy() for _ in range(5)]).arrange(RIGHT, buff=0.8)
        nucleosomes_for_fiber.move_to(LEFT * 2 + DOWN * 1)
        
        self.play(
            FadeOut(nucleosome_element), # Fade out the single nucleosome
            FadeIn(nucleosomes_for_fiber, shift=UP) # Fade in multiple nucleosomes
        )
        self.wait(1)

        # Animate nucleosomes coiling into a chromatin fiber
        # Simplified chromatin fiber: a thicker, more condensed wavy line
        chromatin_fiber_shape = VMobject().set_points_as_corners([
            [-2, 0, 0], [-1.5, 1, 0], [-0.5, -1, 0], [0.5, 1, 0], [1.5, -1, 0], [2, 0, 0]
        ]).set_stroke(CHROMATIN_COLOR, 8).scale(1.5).move_to(nucleosomes_for_fiber.get_center())
        
        # VGroup containing the chromatin fiber shape and its centered text label
        chromatin_element = VGroup(chromatin_fiber_shape, chromatin_label_text.next_to(chromatin_fiber_shape, DOWN, buff=0.5))

        self.play(
            Transform(nucleosomes_for_fiber, chromatin_element) # Transform multiple nucleosomes into the fiber
        )
        self.wait(1.5)

        # --- Part 4: Chromosome Condensation --- 
        chromosome_label_text = Text("Chromosome", font_size=30, color=TEXT_COLOR)
        
        # Helper function to create a single chromatid arm
        def create_chromatid_arm(color):
            arm = VMobject().set_points_as_corners([
                [0, 0, 0], [0.5, 1.5, 0], [0.6, 1.6, 0], [0.7, 1.5, 0], [0.2, 0, 0]
            ]).set_stroke(color, 0).set_fill(color, opacity=0.8)
            return arm

        # Create the four arms of an X-shaped chromosome
        arm1 = create_chromatid_arm(CHROMOSOME_COLOR).rotate(PI/4).shift(LEFT*0.2 + UP*0.2)
        arm2 = create_chromatid_arm(CHROMOSOME_COLOR).rotate(-PI/4).shift(RIGHT*0.2 + UP*0.2)
        arm3 = create_chromatid_arm(CHROMOSOME_COLOR).rotate(PI + PI/4).shift(LEFT*0.2 + DOWN*0.2)
        arm4 = create_chromatid_arm(CHROMOSOME_COLOR).rotate(PI - PI/4).shift(RIGHT*0.2 + DOWN*0.2)
        
        centromere = Circle(radius=0.2, color=CENTROMERE_COLOR, fill_opacity=1).move_to(ORIGIN)
        
        x_chromosome_shape = VGroup(arm1, arm2, arm3, arm4, centromere).scale(1.5).move_to(ORIGIN)
        # VGroup containing the chromosome shape and its centered text label
        x_chromosome_element = VGroup(x_chromosome_shape, chromosome_label_text.next_to(x_chromosome_shape, DOWN, buff=0.5))
        
        self.play(
            Transform(chromatin_element, x_chromosome_element) # Transform chromatin fiber into chromosome
        )
        self.wait(1.5)

        # --- Part 5: Function & Heredity --- 
        genes_label_text = Text("Genes (Genetic Information)", font_size=28, color=TEXT_COLOR)
        
        # Highlight segments on the chromosome as genes
        gene_segment1 = Rectangle(width=0.5, height=0.3, color=GENE_COLOR, fill_opacity=0.7).move_to(arm1.get_center() + UP*0.3 + LEFT*0.1)
        gene_segment2 = Rectangle(width=0.5, height=0.3, color=GENE_COLOR, fill_opacity=0.7).move_to(arm2.get_center() + UP*0.3 + RIGHT*0.1)
        gene_segment3 = Rectangle(width=0.5, height=0.3, color=GENE_COLOR, fill_opacity=0.7).move_to(arm3.get_center() + DOWN*0.3 + LEFT*0.1)
        gene_segment4 = Rectangle(width=0.5, height=0.3, color=GENE_COLOR, fill_opacity=0.7).move_to(arm4.get_center() + DOWN*0.3 + RIGHT*0.1)
        
        genes_group = VGroup(gene_segment1, gene_segment2, gene_segment3, gene_segment4)
        
        self.play(
            FadeIn(genes_group), # Show gene segments
            FadeIn(genes_label_text.next_to(x_chromosome_element, DOWN, buff=1.5)) # Show gene label
        )
        self.wait(2)

        # Show homologous chromosomes for heredity concept
        heredity_label_text = Text("Role in Heredity", font_size=30, color=TEXT_COLOR)
        
        # Create copies of the chromosome and arrange them
        chromosome_copy1_shape = x_chromosome_shape.copy().scale(0.8)
        chromosome_copy2_shape = x_chromosome_shape.copy().scale(0.8)
        
        homologous_chromosomes_shapes = VGroup(chromosome_copy1_shape, chromosome_copy2_shape).arrange(RIGHT, buff=1.5)
        homologous_chromosomes_shapes.move_to(DOWN * 2)

        # Create labels for the copies
        chromosome_copy1_label = Text("From Parent 1", font_size=20, color=TEXT_COLOR).next_to(chromosome_copy1_shape, DOWN, buff=0.3)
        chromosome_copy2_label = Text("From Parent 2", font_size=20, color=TEXT_COLOR).next_to(chromosome_copy2_shape, DOWN, buff=0.3)
        
        # Group all homologous chromosome elements
        homologous_chromosomes_elements = VGroup(homologous_chromosomes_shapes, chromosome_copy1_label, chromosome_copy2_label)
        
        self.play(
            FadeOut(genes_group), # Fade out gene highlights
            FadeOut(genes_label_text), # Fade out gene label
            x_chromosome_element.animate.scale(0.8).move_to(UP*1.5), # Move original chromosome up and scale down
            FadeIn(homologous_chromosomes_elements, shift=DOWN) # Fade in homologous chromosomes
        )
        
        # Text explaining heredity
        heredity_explanation_text = VGroup(
            heredity_label_text.next_to(x_chromosome_element, UP, buff=0.5),
            Text("Carries genetic traits", font_size=24, color=TEXT_COLOR).next_to(heredity_label_text, DOWN, buff=0.3),
            Text("Passed from parents to offspring", font_size=24, color=TEXT_COLOR).next_to(heredity_label_text, DOWN, buff=0.8)
        )
        
        self.play(FadeIn(heredity_explanation_text, shift=UP))
        self.wait(3)

        self.play(FadeOut(VGroup(title, x_chromosome_element, homologous_chromosomes_elements, heredity_explanation_text)))
        self.wait(1)
