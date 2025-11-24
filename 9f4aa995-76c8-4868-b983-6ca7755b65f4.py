import manim

class ChromosomeExplanation(manim.Scene):
    # Custom Chromosome Mobject representing a single chromatid with a centromere.
    # This is used as the basic building block for chromosomes in the animation.
    class Chromosome(manim.VMobject):
        def __init__(self, color=manim.PURPLE_A, width=0.5, height=2.0, centromere_width_factor=0.6, **kwargs):
            super().__init__(**kwargs)
            self.color = color
            self.width = width
            self.height = height
            self.centromere_width_factor = centromere_width_factor

            # Create the main body of the chromatid as a rounded rectangle.
            chromatid = manim.RoundedRectangle(
                corner_radius=width / 2,
                width=width,
                height=height,
                color=color,
                fill_opacity=1.0
            )
            
            # Create the centromere as a smaller rectangle in the middle.
            centromere_height = height * 0.1 # 10% of total height
            centromere = manim.Rectangle(
                width=width * centromere_width_factor,
                height=centromere_height,
                color=manim.RED_A, # Specific color for the centromere
                fill_opacity=1.0
            )
            
            # Position the centromere precisely at the center of the chromatid.
            centromere.move_to(chromatid.get_center())

            # Add both the chromatid body and the centromere to this VGroup.
            self.add(chromatid, centromere)
            self.centromere = centromere
            self.chromatid = chromatid

        # Method to get the centromere Mobject.
        def get_centromere(self):
            return self.centromere

        # Method to get the telomere Mobjects (ends of the chromosome).
        def get_telomeres(self):
            # Create two small circles at the top and bottom ends of the chromatid.
            top_telomere = manim.Circle(radius=self.width/4, color=manim.YELLOW_A, fill_opacity=1.0).move_to(self.chromatid.get_top())
            bottom_telomere = manim.Circle(radius=self.width/4, color=manim.YELLOW_A, fill_opacity=1.0).move_to(self.chromatid.get_bottom())
            return manim.VGroup(top_telomere, bottom_telomere)

    def construct(self):
        # --- Define Colors for consistent styling --- 
        DNA_COLOR = manim.BLUE_E
        CHROMOSOME_COLOR_1 = manim.PURPLE_A
        CHROMOSOME_COLOR_2 = manim.GREEN_A
        GENE_COLOR = manim.ORANGE
        TEXT_COLOR = manim.WHITE
        BACKGROUND_RECT_COLOR = manim.BLACK
        BACKGROUND_RECT_OPACITY = 0.6

        # --- Step 1: Introduction to DNA and Chromosome --- 
        self.next_section("DNA_to_Chromosome", skip_animations=False)
        # Create and display the initial title for the section.
        title = manim.Text("What is a Chromosome?", font_size=48).to_edge(manim.UP)
        self.play(manim.Write(title))
        self.wait(0.5)

        # Create a simplified representation of a DNA double helix.
        dna_helix = manim.VMobject(stroke_width=2, color=DNA_COLOR)
        dna_helix.set_points_as_corners([
            manim.LEFT * 2 + manim.DOWN * 2,
            manim.LEFT * 1 + manim.UP * 2,
            manim.RIGHT * 1 + manim.DOWN * 2,
            manim.RIGHT * 2 + manim.UP * 2
        ])
        dna_helix.scale(1.5).move_to(manim.LEFT * 3)
        
        # Create a label for the DNA helix.
        dna_text = manim.Text("DNA Double Helix", font_size=28, color=DNA_COLOR).next_to(dna_helix, manim.DOWN)
        self.play(manim.Create(dna_helix), manim.Write(dna_text))
        self.wait(1)

        # Create an intermediate shape representing condensed DNA.
        condensed_dna_shape = manim.RoundedRectangle(
            corner_radius=0.25,
            width=0.5,
            height=3.0,
            color=CHROMOSOME_COLOR_1,
            fill_opacity=1.0
        ).move_to(manim.RIGHT * 3)

        # Add an arrow and text to indicate the condensation process.
        condense_arrow = manim.Arrow(dna_helix.get_right(), condensed_dna_shape.get_left(), buff=0.1)
        condense_text = manim.Text("Condensation", font_size=28).next_to(condense_arrow, manim.UP)

        self.play(
            manim.FadeOut(dna_text),
            manim.Create(condense_arrow),
            manim.Write(condense_text)
        )
        # Animate the DNA helix transforming into the condensed shape.
        self.play(
            manim.Transform(dna_helix, condensed_dna_shape),
            run_time=2
        )
        self.wait(1)
        self.play(manim.FadeOut(condense_arrow, condense_text))

        # Transform the condensed DNA shape into the custom Chromosome Mobject,
        # revealing its structured form (with centromere).
        initial_chromosome = self.Chromosome(color=CHROMOSOME_COLOR_1, height=3.0).move_to(manim.ORIGIN)
        self.play(manim.Transform(dna_helix, initial_chromosome))
        self.wait(1)
        
        # Label the newly formed chromosome.
        chromosome_label_text = manim.Text("Chromosome", font_size=28)
        chromosome_label_bg = manim.BackgroundRectangle(chromosome_label_text, color=BACKGROUND_RECT_COLOR, fill_opacity=BACKGROUND_RECT_OPACITY, buff=0.1)
        chromosome_label = manim.VGroup(chromosome_label_bg, chromosome_label_text).next_to(initial_chromosome, manim.DOWN)
        self.play(manim.Write(chromosome_label))
        self.wait(1)
        self.play(manim.FadeOut(dna_helix, chromosome_label)) # Clean up previous elements.

        # --- Step 2: Chromosome Structure --- 
        self.next_section("Chromosome_Structure", skip_animations=False)
        # Update the title for the new section.
        title.become(manim.Text("Chromosome Structure", font_size=48).to_edge(manim.UP))
        self.play(manim.Transform(self.mobjects[0], title)) # Transform the old title Mobject.

        # Create a larger chromosome for detailed labeling.
        chromosome_main = self.Chromosome(color=CHROMOSOME_COLOR_1, height=4.0).move_to(manim.LEFT * 3)
        self.play(manim.Create(chromosome_main))
        self.wait(0.5)

        # Label the Centromere.
        centromere_obj = chromosome_main.get_centromere()
        centromere_label_text = manim.Text("Centromere", font_size=24)
        centromere_label_bg = manim.BackgroundRectangle(centromere_label_text, color=BACKGROUND_RECT_COLOR, fill_opacity=BACKGROUND_RECT_OPACITY, buff=0.1)
        centromere_label = manim.VGroup(centromere_label_bg, centromere_label_text).next_to(centromere_obj, manim.RIGHT, buff=0.5)
        centromere_arrow = manim.Arrow(centromere_label.get_left(), centromere_obj.get_right(), buff=0.1, color=TEXT_COLOR)
        self.play(manim.Create(centromere_arrow), manim.Write(centromere_label))
        self.wait(1)

        # Label the Telomeres.
        telomeres_obj = chromosome_main.get_telomeres()
        self.play(manim.Create(telomeres_obj)) # Show the telomere markers (circles).
        telomere_label_text = manim.Text("Telomeres", font_size=24)
        telomere_label_bg = manim.BackgroundRectangle(telomere_label_text, color=BACKGROUND_RECT_COLOR, fill_opacity=BACKGROUND_RECT_OPACITY, buff=0.1)
        telomere_label = manim.VGroup(telomere_label_bg, telomere_label_text).next_to(telomeres_obj, manim.RIGHT, buff=0.5)
        telomere_arrow = manim.Arrow(telomere_label.get_left(), telomeres_obj.get_right(), buff=0.1, color=TEXT_COLOR)
        self.play(manim.Create(telomere_arrow), manim.Write(telomere_label))
        self.wait(1)

        # Label the entire structure as a Chromatid.
        chromatid_label_text = manim.Text("Chromatid", font_size=24)
        chromatid_label_bg = manim.BackgroundRectangle(chromatid_label_text, color=BACKGROUND_RECT_COLOR, fill_opacity=BACKGROUND_RECT_OPACITY, buff=0.1)
        chromatid_label = manim.VGroup(chromatid_label_bg, chromatid_label_text).next_to(chromosome_main, manim.LEFT, buff=0.5)
        chromatid_arrow = manim.Arrow(chromatid_label.get_right(), chromosome_main.get_left(), buff=0.1, color=TEXT_COLOR)
        self.play(manim.Create(chromatid_arrow), manim.Write(chromatid_label))
        self.wait(2)

        # Fade out all structure labels to prepare for the next section.
        all_structure_labels = manim.VGroup(centromere_label, centromere_arrow, telomere_label, telomere_arrow, chromatid_label, chromatid_arrow, telomeres_obj)
        self.play(manim.FadeOut(all_structure_labels))

        # --- Step 3: Homologous Chromosomes --- 
        self.next_section("Homologous_Chromosomes", skip_animations=False)
        # Update the title.
        title.become(manim.Text("Homologous Chromosomes", font_size=48).to_edge(manim.UP))
        self.play(manim.Transform(self.mobjects[0], title))
        # Scale down and reposition the existing chromosome.
        self.play(chromosome_main.animate.scale(0.8).to_edge(manim.LEFT).shift(manim.UP * 0.5))

        # Create a second chromosome, representing the paternal one, with a different color.
        chromosome_mom = chromosome_main.copy().set_color(CHROMOSOME_COLOR_1) # Maternal chromosome
        chromosome_dad = self.Chromosome(color=CHROMOSOME_COLOR_2, height=chromosome_mom.height, width=chromosome_mom.width).next_to(chromosome_mom, manim.RIGHT, buff=1.0) # Paternal chromosome

        # Label the maternal chromosome.
        mom_label_text = manim.Text("Maternal", font_size=24, color=CHROMOSOME_COLOR_1)
        mom_label_bg = manim.BackgroundRectangle(mom_label_text, color=BACKGROUND_RECT_COLOR, fill_opacity=BACKGROUND_RECT_OPACITY, buff=0.1)
        mom_label = manim.VGroup(mom_label_bg, mom_label_text).next_to(chromosome_mom, manim.DOWN)

        # Label the paternal chromosome.
        dad_label_text = manim.Text("Paternal", font_size=24, color=CHROMOSOME_COLOR_2)
        dad_label_bg = manim.BackgroundRectangle(dad_label_text, color=BACKGROUND_RECT_COLOR, fill_opacity=BACKGROUND_RECT_OPACITY, buff=0.1)
        dad_label = manim.VGroup(dad_label_bg, dad_label_text).next_to(chromosome_dad, manim.DOWN)

        self.play(manim.Create(chromosome_dad), manim.Write(mom_label), manim.Write(dad_label))
        self.wait(1)

        # Add a label for the homologous pair.
        homologous_pair_label_text = manim.Text("Homologous Pair", font_size=36)
        homologous_pair_label_bg = manim.BackgroundRectangle(homologous_pair_label_text, color=BACKGROUND_RECT_COLOR, fill_opacity=BACKGROUND_RECT_OPACITY, buff=0.1)
        homologous_pair_label = manim.VGroup(homologous_pair_label_bg, homologous_pair_label_text).next_to(manim.VGroup(chromosome_mom, chromosome_dad), manim.DOWN, buff=1.0)
        self.play(manim.Write(homologous_pair_label))
        self.wait(2)

        # --- Step 4: Genes on Chromosomes --- 
        self.next_section("Genes_on_Chromosomes", skip_animations=False)
        # Update the title.
        title.become(manim.Text("Genes on Chromosomes", font_size=48).to_edge(manim.UP))
        self.play(manim.Transform(self.mobjects[0], title))
        # Fade out previous labels and reposition the chromosome pair.
        self.play(
            manim.FadeOut(mom_label, dad_label, homologous_pair_label),
            manim.VGroup(chromosome_mom, chromosome_dad).animate.center().shift(manim.UP * 0.5)
        )
        self.wait(0.5)

        # Define relative positions for genes along the chromosome.
        gene_positions_factors = [0.3, -0.1, -0.4] # Factors relative to half chromosome height.

        genes_mom = manim.VGroup()
        genes_dad = manim.VGroup()
        gene_labels_group = manim.VGroup() # Group to hold all gene labels and their arrows.

        gene_names = ["Gene A", "Gene B", "Gene C"]

        # Iterate to create and position genes and their labels.
        for i, pos_factor in enumerate(gene_positions_factors):
            # Create gene rectangles on the maternal chromosome.
            gene_rect_mom = manim.Rectangle(width=0.4, height=0.2, color=GENE_COLOR, fill_opacity=1.0)
            gene_rect_mom.move_to(chromosome_mom.get_center() + manim.UP * pos_factor * chromosome_mom.height / 2)
            genes_mom.add(gene_rect_mom)

            # Create corresponding gene rectangles on the paternal chromosome.
            gene_rect_dad = manim.Rectangle(width=0.4, height=0.2, color=GENE_COLOR, fill_opacity=1.0)
            gene_rect_dad.move_to(chromosome_dad.get_center() + manim.UP * pos_factor * chromosome_dad.height / 2)
            genes_dad.add(gene_rect_dad)

            # Create a label for the gene.
            gene_label_text = manim.Text(gene_names[i], font_size=20)
            gene_label_bg = manim.BackgroundRectangle(gene_label_text, color=BACKGROUND_RECT_COLOR, fill_opacity=BACKGROUND_RECT_OPACITY, buff=0.05)
            gene_label = manim.VGroup(gene_label_bg, gene_label_text).next_to(gene_rect_mom, manim.LEFT, buff=0.3)
            gene_arrow = manim.Arrow(gene_label.get_right(), gene_rect_mom.get_left(), buff=0.05, color=TEXT_COLOR, stroke_width=2)
            
            gene_labels_group.add(gene_label, gene_arrow)

        self.play(manim.Create(genes_mom), manim.Create(genes_dad))
        self.play(manim.Create(gene_labels_group))
        self.wait(2)

        # Add an explanation for genes.
        gene_explanation = manim.Text(
            "Genes are specific locations on chromosomes\nthat determine traits.",
            font_size=28,
            line_spacing=1.2
        ).next_to(manim.VGroup(chromosome_mom, chromosome_dad), manim.DOWN, buff=1.0)
        self.play(manim.Write(gene_explanation))
        self.wait(3)

        self.play(manim.FadeOut(genes_mom, genes_dad, gene_labels_group, gene_explanation))

        # --- Step 5: Sex Chromosomes --- 
        self.next_section("Sex_Chromosomes", skip_animations=False)
        # Update the title.
        title.become(manim.Text("Sex Chromosomes", font_size=48).to_edge(manim.UP))
        self.play(manim.Transform(self.mobjects[0], title))
        # Reset scale and position of the chromosome pair.
        self.play(manim.VGroup(chromosome_mom, chromosome_dad).animate.scale(1/0.8).center().shift(manim.UP * 0.5))

        # Create an XX pair (female).
        x_chromosome_1 = self.Chromosome(color=CHROMOSOME_COLOR_1, height=3.5)
        x_chromosome_2 = self.Chromosome(color=CHROMOSOME_COLOR_2, height=3.5)
        
        xx_pair = manim.VGroup(x_chromosome_1, x_chromosome_2).arrange(manim.RIGHT, buff=1.0).move_to(manim.LEFT * 3)
        xx_label_text = manim.Text("XX (Female)", font_size=36)
        xx_label_bg = manim.BackgroundRectangle(xx_label_text, color=BACKGROUND_RECT_COLOR, fill_opacity=BACKGROUND_RECT_OPACITY, buff=0.1)
        xx_label = manim.VGroup(xx_label_bg, xx_label_text).next_to(xx_pair, manim.DOWN)

        self.play(manim.Create(xx_pair), manim.Write(xx_label))
        self.wait(2);

        # Create an XY pair (male).
        x_chromosome_male = self.Chromosome(color=CHROMOSOME_COLOR_1, height=3.5)
        y_chromosome_male = self.Chromosome(color=CHROMOSOME_COLOR_2, height=2.0, width=0.4) # Y chromosome is typically smaller.
        
        xy_pair = manim.VGroup(x_chromosome_male, y_chromosome_male).arrange(manim.RIGHT, buff=1.0).move_to(manim.RIGHT * 3)
        xy_label_text = manim.Text("XY (Male)", font_size=36)
        xy_label_bg = manim.BackgroundRectangle(xy_label_text, color=BACKGROUND_RECT_COLOR, fill_opacity=BACKGROUND_RECT_OPACITY, buff=0.1)
        xy_label = manim.VGroup(xy_label_bg, xy_label_text).next_to(xy_pair, manim.DOWN)

        # Transform the XX pair and its label into the XY pair and its label.
        self.play(
            manim.Transform(xx_pair, xy_pair),
            manim.Transform(xx_label, xy_label)
        )
        self.wait(3)

        # Display a concluding message.
        final_text = manim.Text("Chromosomes carry our genetic information!", font_size=36).to_edge(manim.DOWN)
        self.play(manim.Write(final_text))
        self.wait(3)

        # Fade out all remaining mobjects to end the scene.
        self.play(manim.FadeOut(*self.mobjects))
        self.wait(1)
