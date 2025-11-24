import manim

# Define custom VGroups for reusability and cleaner code
class Chromosome(manim.VGroup):
    def __init__(self, color=manim.PURPLE, label_text="Chromosome", scale_factor=1.0, **kwargs):
        super().__init__(**kwargs)
        # Two arms forming the 'X' shape
        arm1 = manim.RoundedRectangle(width=0.5, height=2, corner_radius=0.25, color=color, fill_opacity=0.8)
        arm2 = manim.RoundedRectangle(width=0.5, height=2, corner_radius=0.25, color=color, fill_opacity=0.8)
        arm1.rotate(manim.PI/4)
        arm2.rotate(-manim.PI/4)

        # Centromere (optional, but adds detail)
        centromere = manim.Circle(radius=0.15, color=color, fill_opacity=1).move_to(manim.ORIGIN)

        # Group the visual body of the chromosome
        chromosome_body = manim.VGroup(arm1, arm2, centromere).scale(scale_factor)

        # Label for the chromosome
        label = manim.Text(label_text, font_size=28, color=color).next_to(chromosome_body, manim.DOWN, buff=0.2)

        self.add(chromosome_body, label)
        self.chromosome_body = chromosome_body # Store the visual part for positioning genes
        self.label_mobject = label # Store the text mobject for updates

    def get_gene_position(self, relative_y_offset):
        # Calculate a position along the chromosome body for a gene marker
        # relative_y_offset: -1 (bottom) to 1 (top), 0 (center)
        # We use 0.7 to ensure genes are placed within the visible arms, not at the very tip
        return self.chromosome_body.get_center() + manim.UP * relative_y_offset * (self.chromosome_body.height / 2 * 0.7)

class GeneMarker(manim.VGroup):
    def __init__(self, text_content, position, color=manim.YELLOW, text_color=manim.BLACK, font_size=20, **kwargs):
        super().__init__(**kwargs)
        # Rectangle representing the gene locus
        rect = manim.Rectangle(width=0.6, height=0.3, color=color, fill_opacity=0.8).move_to(position)
        # Text label for the gene
        text = manim.Text(text_content, font_size=font_size, color=text_color).move_to(rect.get_center())
        self.add(rect, text)
        self.rect = rect # Store the rectangle for positioning
        self.text_mobject = text # Store the text mobject for updates

    def update_text_animation(self, new_text_content):
        # Creates an animation to update the gene's text label
        new_text = manim.Text(new_text_content, font_size=self.text_mobject.font_size, color=self.text_mobject.color)
        new_text.move_to(self.rect.get_center()) # Ensure new text is centered on the rectangle
        return manim.Transform(self.text_mobject, new_text)


class ChromosomeExplanation(manim.Scene):
    def construct(self):
        # --- Part 1: Introduction to DNA and Chromosomes ---
        title_dna = manim.Text("DNA: The Blueprint of Life", font_size=48).to_edge(manim.UP)
        self.play(manim.Write(title_dna))
        self.wait(0.5)

        # Simplified DNA strand (two parallel wavy lines)
        dna_strand_left = manim.VMobject().set_points_as_corners([
            [-3, -1, 0], [-2.5, 0, 0], [-2, -1, 0], [-1.5, 0, 0], [-1, -1, 0], [-0.5, 0, 0], [0, -1, 0]
        ]).set_stroke(manim.BLUE, width=3)
        dna_strand_right = manim.VMobject().set_points_as_corners([
            [-3, 1, 0], [-2.5, 0, 0], [-2, 1, 0], [-1.5, 0, 0], [-1, 1, 0], [-0.5, 0, 0], [0, 1, 0]
        ]).set_stroke(manim.BLUE, width=3)
        dna_strand = manim.VGroup(dna_strand_left, dna_strand_right).scale(1.5).next_to(title_dna, manim.DOWN, buff=1)

        self.play(manim.Create(dna_strand))
        self.wait(1)

        # Explain DNA coiling into a chromosome
        coiling_text = manim.Text("DNA coils tightly...", font_size=32).next_to(dna_strand, manim.DOWN, buff=0.5)
        self.play(manim.Write(coiling_text))
        self.wait(1)

        # Create a chromosome object
        initial_chromosome = Chromosome(color=manim.PURPLE, label_text="Chromosome", scale_factor=0.8)
        initial_chromosome.move_to(dna_strand.get_center())
        
        # Animate the creation of the entire Chromosome VGroup
        self.play(
            manim.FadeOut(dna_strand),
            manim.Transform(coiling_text, manim.Text("...to form a Chromosome", font_size=32).move_to(coiling_text.get_center())),
            manim.Create(initial_chromosome) # Create the entire VGroup
        )
        self.wait(1.5)
        self.play(manim.FadeOut(title_dna), manim.FadeOut(coiling_text)) # Clean up intro texts

        # --- Part 2: Homologous Chromosomes ---
        # Move the initial chromosome to the left, scaling it down
        self.play(initial_chromosome.animate.scale(0.8).to_edge(manim.LEFT, buff=1.5).shift(manim.UP*0.5))
        self.wait(0.5) # Small pause for clarity

        # Define the target states for maternal and paternal chromosomes
        # These will be arranged to determine their final positions.
        maternal_chrom_target = Chromosome(color=manim.RED_B, label_text="Maternal", scale_factor=0.8)
        paternal_chrom_target = Chromosome(color=manim.BLUE_B, label_text="Paternal", scale_factor=0.8)

        # Arrange them as a pair to get their final positions
        # This VGroup is temporary, just for positioning.
        temp_pair_for_positioning = manim.VGroup(maternal_chrom_target, paternal_chrom_target).arrange(manim.RIGHT, buff=1.5).center()
        homologous_pair_label = manim.Text("Homologous Chromosomes", font_size=36).next_to(temp_pair_for_positioning, manim.UP, buff=0.8)

        # Now, transform the moved initial_chromosome into the maternal_chrom_target
        # and create the paternal_chrom_target at their arranged positions.
        self.play(
            manim.Transform(initial_chromosome, maternal_chrom_target), # initial_chromosome transforms into maternal_chrom_target
            manim.Create(paternal_chrom_target), # paternal_chrom_target appears
            manim.Write(homologous_pair_label)
        )
        self.wait(1.5)

        # After the transform, initial_chromosome has been transformed into maternal_chrom_target.
        # The variable `maternal_chrom_target` now holds the mobject that is visually on screen
        # and represents the maternal chromosome.
        # The variable `paternal_chrom_target` also holds the mobject that is visually on screen.

        # Create a VGroup from the actual mobjects on screen for collective animation
        # It's crucial to use the target mobjects (maternal_chrom_target, paternal_chrom_target)
        # as they now represent the objects on the scene after the transformation/creation.
        homologous_pair_on_screen = manim.VGroup(maternal_chrom_target, paternal_chrom_target)

        # --- Part 3: Genes and Alleles ---
        self.play(homologous_pair_on_screen.animate.shift(manim.DOWN*0.5)) # Shift down to make space for gene labels

        # Gene A on maternal chromosome (using the live mobject, which is maternal_chrom_target)
        gene_a_maternal = GeneMarker("Gene A", maternal_chrom_target.get_gene_position(0.5), color=manim.YELLOW)
        # Gene B on maternal chromosome
        gene_b_maternal = GeneMarker("Gene B", maternal_chrom_target.get_gene_position(-0.5), color=manim.GREEN)

        # Gene A on paternal chromosome
        gene_a_paternal = GeneMarker("Gene A", paternal_chrom_target.get_gene_position(0.5), color=manim.YELLOW)
        # Gene B on paternal chromosome
        gene_b_paternal = GeneMarker("Gene B", paternal_chrom_target.get_gene_position(-0.5), color=manim.GREEN)

        genes_on_chromosomes = manim.VGroup(
            gene_a_maternal, gene_b_maternal,
            gene_a_paternal, gene_b_paternal
        )

        genes_label = manim.Text("Genes: Specific locations on chromosomes", font_size=32).next_to(homologous_pair_label, manim.UP, buff=0.5)
        self.play(
            manim.FadeOut(homologous_pair_label),
            manim.Write(genes_label),
            manim.Create(genes_on_chromosomes)
        )
        self.wait(1.5)

        # Introduce Alleles
        alleles_label = manim.Text("Alleles: Different versions of a gene", font_size=32).next_to(genes_label, manim.UP, buff=0.5)

        self.play(
            manim.FadeOut(genes_label),
            manim.Write(alleles_label),
            gene_a_maternal.update_text_animation("Allele A1"),
            gene_a_paternal.update_text_animation("Allele A2"),
            gene_b_maternal.update_text_animation("Allele B1"),
            gene_b_paternal.update_text_animation("Allele B2")
        )
        self.wait(2)

        # Final cleanup
        self.play(manim.FadeOut(self.mobjects))
        self.wait(0.5)