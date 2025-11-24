from manim import *

class ChromosomesExplanation(Scene):
    def construct(self):
        # --- Part 1: What is a Chromosome? --- 
        # Create the main body of a chromosome as a rounded rectangle
        chromosome_body = RoundedRectangle(
            width=1.0, height=3.0, corner_radius=0.2, color=BLUE_E, fill_opacity=0.8
        )
        # Create a text label for the chromosome and center it on the body
        chromosome_label = Text("Chromosome", font_size=36).move_to(chromosome_body.get_center())
        # Group the body and its label together
        chromosome_vg = VGroup(chromosome_body, chromosome_label)

        # Animate the creation of the chromosome
        self.play(Create(chromosome_vg))
        self.wait(0.5)
        # Shift the chromosome upwards to make space below
        self.play(chromosome_vg.animate.shift(UP * 1.5))

        # Add text indicating that chromosomes contain DNA
        dna_text = Text("Contains DNA", font_size=30).next_to(chromosome_vg, DOWN, buff=0.5)
        self.play(Write(dna_text))
        self.wait(1)

        # --- Part 2: DNA Structure (Simplified) --- 
        # Define colors for the double helix strands
        helix_color_1 = GOLD_E
        helix_color_2 = MAROON_E
        num_points = 50 # Number of points to define the helix curves
        amplitude = 0.3 # Amplitude of the sine wave for the helix
        frequency = 2 # Frequency of the sine wave
        length = 2.0 # Length of the helix

        # Generate points for the first helix strand
        helix1_points = [
            [x, amplitude * np.sin(frequency * x), 0]
            for x in np.linspace(-length / 2, length / 2, num_points)
        ]
        # Generate points for the second helix strand (out of phase)
        helix2_points = [
            [x, amplitude * np.sin(frequency * x + np.pi), 0]
            for x in np.linspace(-length / 2, length / 2, num_points)
        ]

        # Create VMobject paths for the helix strands
        helix1 = VMobject().set_points_as_corners(helix1_points).set_color(helix_color_1)
        helix2 = VMobject().set_points_as_corners(helix2_points).set_color(helix_color_2)

        # Add "rungs" to simulate the ladder structure of DNA
        rungs = VGroup()
        for i in range(0, num_points, 5): # Draw rungs every few points
            rung = Line(helix1_points[i], helix2_points[i], color=GREY_B)
            rungs.add(rung)

        # Group the helix strands and rungs, scale, and position them below the DNA text
        dna_helix_vg = VGroup(helix1, helix2, rungs).scale(0.7)
        dna_helix_vg.move_to(dna_text.get_center() + DOWN * 1.5) # Position below DNA text

        # Animate the fading in of the DNA helix
        self.play(FadeIn(dna_helix_vg, shift=UP))
        self.wait(1.5)
        # Fade out the DNA helix and text, then move the chromosome back to the center
        self.play(FadeOut(dna_helix_vg, dna_text))
        self.play(chromosome_vg.animate.move_to(ORIGIN))
        self.wait(0.5)

        # --- Part 3: Genes on a Chromosome --- 
        # Define common properties for gene rectangles
        gene_rect_width = chromosome_body.get_width() * 0.8
        gene_rect_height = 0.3
        gene_color = YELLOW_B

        # Create Gene A (rectangle + label)
        gene_a_rect = Rectangle(width=gene_rect_width, height=gene_rect_height, color=gene_color, fill_opacity=0.7)
        gene_a_rect.move_to(chromosome_body.get_top() + DOWN * 0.7)
        gene_a_label = Text("Gene A", font_size=24).move_to(gene_a_rect.get_center())
        gene_a_vg = VGroup(gene_a_rect, gene_a_label)

        # Create Gene B (rectangle + label)
        gene_b_rect = Rectangle(width=gene_rect_width, height=gene_rect_height, color=gene_color, fill_opacity=0.7)
        gene_b_rect.move_to(chromosome_body.get_center())
        gene_b_label = Text("Gene B", font_size=24).move_to(gene_b_rect.get_center())
        gene_b_vg = VGroup(gene_b_rect, gene_b_label)

        # Create Gene C (rectangle + label)
        gene_c_rect = Rectangle(width=gene_rect_width, height=gene_rect_height, color=gene_color, fill_opacity=0.7)
        gene_c_rect.move_to(chromosome_body.get_bottom() + UP * 0.7)
        gene_c_label = Text("Gene C", font_size=24).move_to(gene_c_rect.get_center())
        gene_c_vg = VGroup(gene_c_rect, gene_c_label)

        # Group all genes together
        genes_on_chromosome = VGroup(gene_a_vg, gene_b_vg, gene_c_vg)

        # Animate the fading in of the genes
        self.play(FadeIn(genes_on_chromosome, shift=UP))
        self.wait(1)

        # Add an explanation text for genes
        gene_explanation_text = Text(
            "Genes are specific segments of DNA that carry instructions for traits.",
            font_size=28
        ).to_edge(DOWN)
        self.play(Write(gene_explanation_text))
        self.wait(2)
        self.play(FadeOut(gene_explanation_text))
        self.wait(0.5)

        # --- Part 4: Homologous Chromosomes --- 
        # Create a copy of the chromosome and its genes for the homologous pair
        homologous_chromosome_vg = chromosome_vg.copy().shift(RIGHT * 3)
        homologous_genes_on_chromosome = genes_on_chromosome.copy().shift(RIGHT * 3)

        # Create new labels for the chromosomes to indicate their origin
        original_chromosome_label_new = Text("Chromosome (from Parent 1)", font_size=28).next_to(chromosome_vg, UP, buff=0.3)
        homologous_chromosome_label_new = Text("Chromosome (from Parent 2)", font_size=28).next_to(homologous_chromosome_vg, UP, buff=0.3)

        # Animate the separation of the original chromosome and the introduction of its homologous pair
        self.play(
            chromosome_vg.animate.shift(LEFT * 3), # Move original chromosome left
            FadeIn(homologous_chromosome_vg, homologous_genes_on_chromosome), # Fade in the homologous chromosome and its genes
            ReplacementTransform(chromosome_vg[1], original_chromosome_label_new), # Transform original label
            Create(homologous_chromosome_label_new) # Create new label for homologous chromosome
        )
        # Update the VGroup's label reference after transformation
        chromosome_vg[1].become(original_chromosome_label_new)
        # Add the new label to the homologous chromosome VGroup
        homologous_chromosome_vg.add(homologous_chromosome_label_new)

        # Add explanation text for homologous chromosomes
        homologous_pair_text = Text(
            "Humans have 23 pairs of homologous chromosomes.",
            font_size=28
        ).to_edge(DOWN)
        self.play(Write(homologous_pair_text))
        self.wait(2)
        self.play(FadeOut(homologous_pair_text))
        self.wait(0.5)

        # Group all visible chromosomes and genes for scaling
        all_chromosomes_and_genes = VGroup(
            chromosome_vg, genes_on_chromosome,
            homologous_chromosome_vg, homologous_genes_on_chromosome
        )
        # Scale down and move to the top edge to make space for replication animation
        self.play(all_chromosomes_and_genes.animate.scale(0.7).to_edge(UP))
        self.wait(0.5)

        # --- Part 5: Chromosome Replication --- 
        # Create a temporary VGroup for the chromosome and its genes to animate its isolation
        # This VGroup includes the chromosome body, its updated label, and its genes
        chromosome_to_replicate = VGroup(chromosome_vg[0], chromosome_vg[1], genes_on_chromosome)
        
        # Animate fading other elements and bringing the chosen chromosome to the center
        self.play(
            all_chromosomes_and_genes.animate.fade(0.5), # Fade other elements
            chromosome_to_replicate.animate.scale(1/0.7).move_to(ORIGIN) # Bring to center and original size
        )
        self.wait(0.5)

        # Create the components of the replicated chromosome (sister chromatids)
        # Target state for the first chromatid (derived from the original chromosome)
        first_chromatid_body_target = chromosome_vg[0].copy().scale(0.8).shift(LEFT * 0.5)
        first_chromatid_label_target = Text("Chromatid 1", font_size=24).move_to(first_chromatid_body_target.get_center())
        first_chromatid_genes_target = genes_on_chromosome.copy().scale(0.8).shift(LEFT * 0.5)
        
        # Components for the second chromatid (the newly replicated copy)
        second_chromatid_body = chromosome_vg[0].copy().scale(0.8).shift(RIGHT * 0.5)
        second_chromatid_label = Text("Chromatid 2", font_size=24).move_to(second_chromatid_body.get_center())
        second_chromatid_genes = genes_on_chromosome.copy().scale(0.8).shift(RIGHT * 0.5)

        # Centromere (the constricted region joining sister chromatids)
        centromere = Circle(radius=0.15, color=RED, fill_opacity=1).move_to(ORIGIN)
        centromere_label = Text("Centromere", font_size=24).next_to(centromere, DOWN, buff=0.2)
        centromere_vg = VGroup(centromere, centromere_label)

        # Animate the replication process
        self.play(
            Transform(chromosome_vg[0], first_chromatid_body_target), # Transform original body into first chromatid body
            Transform(genes_on_chromosome, first_chromatid_genes_target), # Transform original genes into first chromatid genes
            FadeOut(chromosome_vg[1]), # Fade out the old chromosome label
            Create(first_chromatid_label_target), # Create new label for chromatid 1
            Create(VGroup(second_chromatid_body, second_chromatid_label)), # Create second chromatid body and label
            Create(second_chromatid_genes), # Create genes for second chromatid
            Create(centromere_vg) # Create centromere
        )
        
        # Group all parts of the replicated chromosome for later fading
        replicated_chromosome_vg = VGroup(
            first_chromatid_body_target, first_chromatid_label_target, first_chromatid_genes_target,
            second_chromatid_body, second_chromatid_label, second_chromatid_genes,
            centromere_vg
        )

        # Add explanation text for chromosome replication
        replication_text = Text(
            "Before cell division, chromosomes replicate to form two identical sister chromatids.",
            font_size=28
        ).to_edge(DOWN)
        self.play(Write(replication_text))
        self.wait(3)
        self.play(FadeOut(replication_text))
        self.wait(0.5)

        # --- Part 6: Conclusion --- 
        # Fade out all elements from the replication step and the faded background elements
        self.play(FadeOut(replicated_chromosome_vg, all_chromosomes_and_genes))

        # Display a final concluding statement
        final_text = Text(
            "Chromosomes are fundamental for heredity, carrying our genetic blueprint.",
            font_size=36,
            color=WHITE
        ).scale(0.8)
        self.play(Write(final_text))
        self.wait(3)
        self.play(FadeOut(final_text))
