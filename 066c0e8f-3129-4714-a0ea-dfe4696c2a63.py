from manim import *

# Define custom VGroups for reusability and cleaner code
class Chromosome(VGroup):
    def __init__(self, color=PURPLE, label_text="Chromosome", scale_factor=1.0, **kwargs):
        super().__init__(**kwargs)
        # Two arms forming the 'X' shape
        arm1 = RoundedRectangle(width=0.5, height=2, corner_radius=0.25, color=color, fill_opacity=0.8)
        arm2 = RoundedRectangle(width=0.5, height=2, corner_radius=0.25, color=color, fill_opacity=0.8)
        arm1.rotate(PI/4)
        arm2.rotate(-PI/4)

        # Centromere (optional, but adds detail)
        centromere = Circle(radius=0.15, color=color, fill_opacity=1).move_to(ORIGIN)

        # Group the visual body of the chromosome
        chromosome_body = VGroup(arm1, arm2, centromere).scale(scale_factor)

        # Label for the chromosome
        label = Text(label_text, font_size=28, color=color).next_to(chromosome_body, DOWN, buff=0.2)

        self.add(chromosome_body, label)
        self.chromosome_body = chromosome_body # Store the visual part for positioning genes
        self.label_mobject = label # Store the text mobject for updates

    def get_gene_position(self, relative_y_offset):
        # Calculate a position along the chromosome body for a gene marker
        # relative_y_offset: -1 (bottom) to 1 (top), 0 (center)
        # We use 0.7 to ensure genes are placed within the visible arms, not at the very tip
        return self.chromosome_body.get_center() + UP * relative_y_offset * (self.chromosome_body.height / 2 * 0.7)

class GeneMarker(VGroup):
    def __init__(self, text_content, position, color=YELLOW, text_color=BLACK, font_size=20, **kwargs):
        super().__init__(**kwargs)
        # Rectangle representing the gene locus
        rect = Rectangle(width=0.6, height=0.3, color=color, fill_opacity=0.8).move_to(position)
        # Text label for the gene
        text = Text(text_content, font_size=font_size, color=text_color).move_to(rect.get_center())
        self.add(rect, text)
        self.rect = rect # Store the rectangle for positioning
        self.text_mobject = text # Store the text mobject for updates

    def update_text_animation(self, new_text_content):
        # Creates an animation to update the gene's text label
        new_text = Text(new_text_content, font_size=self.text_mobject.font_size, color=self.text_mobject.color)
        new_text.move_to(self.rect.get_center()) # Ensure new text is centered on the rectangle
        return Transform(self.text_mobject, new_text)


class ChromosomeExplanation(Scene):
    def construct(self):
        # --- Part 1: Introduction to DNA and Chromosomes ---
        title_dna = Text("DNA: The Blueprint of Life", font_size=48).to_edge(UP)
        self.play(Write(title_dna))
        self.wait(0.5)

        # Simplified DNA strand (two parallel wavy lines)
        dna_strand_left = VMobject().set_points_as_corners([
            [-3, -1, 0], [-2.5, 0, 0], [-2, -1, 0], [-1.5, 0, 0], [-1, -1, 0], [-0.5, 0, 0], [0, -1, 0]
        ]).set_stroke(BLUE, width=3)
        dna_strand_right = VMobject().set_points_as_corners([
            [-3, 1, 0], [-2.5, 0, 0], [-2, 1, 0], [-1.5, 0, 0], [-1, 1, 0], [-0.5, 0, 0], [0, 1, 0]
        ]).set_stroke(BLUE, width=3)
        dna_strand = VGroup(dna_strand_left, dna_strand_right).scale(1.5).next_to(title_dna, DOWN, buff=1)

        self.play(Create(dna_strand))
        self.wait(1)

        # Explain DNA coiling into a chromosome
        coiling_text = Text("DNA coils tightly...", font_size=32).next_to(dna_strand, DOWN, buff=0.5)
        self.play(Write(coiling_text))
        self.wait(1)

        # Create a chromosome object
        initial_chromosome = Chromosome(color=PURPLE, label_text="Chromosome", scale_factor=0.8)
        initial_chromosome.move_to(dna_strand.get_center())

        self.play(
            FadeOut(dna_strand),
            Transform(coiling_text, Text("...to form a Chromosome", font_size=32).move_to(coiling_text.get_center())),
            Create(initial_chromosome.chromosome_body), # Create the shape first
            Write(initial_chromosome.label_mobject) # Then write its label
        )
        self.wait(1.5)
        self.play(FadeOut(title_dna), FadeOut(coiling_text)) # Clean up intro texts

        # --- Part 2: Homologous Chromosomes ---
        # Move the first chromosome to the left
        self.play(initial_chromosome.animate.scale(0.8).to_edge(LEFT, buff=1.5).shift(UP*0.5))

        # Create maternal and paternal chromosomes
        maternal_chrom = Chromosome(color=RED_B, label_text="Maternal", scale_factor=0.8)
        paternal_chrom = Chromosome(color=BLUE_B, label_text="Paternal", scale_factor=0.8)

        # Arrange them as a pair
        homologous_pair = VGroup(maternal_chrom, paternal_chrom).arrange(RIGHT, buff=1.5).center()
        homologous_pair_label = Text("Homologous Chromosomes", font_size=36).next_to(homologous_pair, UP, buff=0.8)

        self.play(
            Transform(initial_chromosome, maternal_chrom), # Transform the initial chromosome into the maternal one
            Create(paternal_chrom), # Create the paternal one
            Write(homologous_pair_label)
        )
        self.wait(1.5);

        # --- Part 3: Genes and Alleles ---
        self.play(homologous_pair.animate.shift(DOWN*0.5)) # Shift down to make space for gene labels

        # Gene A on maternal chromosome
        gene_a_maternal = GeneMarker("Gene A", maternal_chrom.get_gene_position(0.5), color=YELLOW)
        # Gene B on maternal chromosome
        gene_b_maternal = GeneMarker("Gene B", maternal_chrom.get_gene_position(-0.5), color=GREEN)

        # Gene A on paternal chromosome
        gene_a_paternal = GeneMarker("Gene A", paternal_chrom.get_gene_position(0.5), color=YELLOW)
        # Gene B on paternal chromosome
        gene_b_paternal = GeneMarker("Gene B", paternal_chrom.get_gene_position(-0.5), color=GREEN)

        genes_on_chromosomes = VGroup(
            gene_a_maternal, gene_b_maternal,
            gene_a_paternal, gene_b_paternal
        )

        genes_label = Text("Genes: Specific locations on chromosomes", font_size=32).next_to(homologous_pair_label, UP, buff=0.5)
        self.play(
            FadeOut(homologous_pair_label),
            Write(genes_label),
            Create(genes_on_chromosomes)
        )
        self.wait(1.5)

        # Introduce Alleles
        alleles_label = Text("Alleles: Different versions of a gene", font_size=32).next_to(genes_label, UP, buff=0.5)

        self.play(
            FadeOut(genes_label),
            Write(alleles_label),
            gene_a_maternal.update_text_animation("Allele A1"),
            gene_a_paternal.update_text_animation("Allele A2"),
            gene_b_maternal.update_text_animation("Allele B1"),
            gene_b_paternal.update_text_animation("Allele B2")
        )
        self.wait(2)

        # Final cleanup
        self.play(FadeOut(self.mobjects))
        self.wait(0.5)
