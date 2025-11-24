from manim import *
import random

# Custom Mobject for a single chromatid (one arm of an X-shaped chromosome)
class Chromatid(VGroup):
    def __init__(self, color=BLUE, p_arm_length=0.6, q_arm_length=0.8, width=0.2, centromere_height=0.2, **kwargs):
        super().__init__(**kwargs)
        
        # p-arm (short arm, usually top)
        p_arm = RoundedRectangle(width=width, height=p_arm_length, corner_radius=width/2, color=color, fill_opacity=0.8)
        # q-arm (long arm, usually bottom)
        q_arm = RoundedRectangle(width=width, height=q_arm_length, corner_radius=width/2, color=color, fill_opacity=0.8)
        # Centromere segment (the constricted region)
        centromere_segment = Rectangle(width=width * 1.2, height=centromere_height, color=color, fill_opacity=0.8)

        # Arrange the arms and centromere vertically
        p_arm.next_to(centromere_segment, UP, buff=0)
        q_arm.next_to(centromere_segment, DOWN, buff=0)

        self.add(p_arm, q_arm, centromere_segment)
        self.center() # Center the entire chromatid mobject

# Custom Mobject for a duplicated chromosome (X-shape)
class DuplicatedChromosome(VGroup):
    def __init__(self, color=BLUE, p_arm_length=0.6, q_arm_length=0.8, width=0.2, centromere_height=0.2, **kwargs):
        super().__init__(**kwargs)
        
        # Create two sister chromatids with specified arm lengths
        chromatid1 = Chromatid(color=color, p_arm_length=p_arm_length, q_arm_length=q_arm_length, width=width, centromere_height=centromere_height)
        chromatid2 = chromatid1.copy()

        # Rotate them slightly to form the characteristic X-shape
        # The rotation is around their individual centers (where the centromere is)
        chromatid1.rotate(PI/8)
        chromatid2.rotate(-PI/8)

        self.add(chromatid1, chromatid2)
        self.center() # Center the entire duplicated chromosome mobject

# Specific Mobject for an X chromosome
class XChromosome(DuplicatedChromosome):
    def __init__(self, color=BLUE, **kwargs):
        # X chromosomes typically have two relatively similar-length arms (p and q)
        super().__init__(color=color, p_arm_length=0.6, q_arm_length=0.8, width=0.2, centromere_height=0.2, **kwargs)

# Specific Mobject for a Y chromosome
class YChromosome(DuplicatedChromosome):
    def __init__(self, color=RED, **kwargs):
        # Y chromosomes have a very short p-arm and a longer q-arm, making them smaller overall
        super().__init__(color=color, p_arm_length=0.2, q_arm_length=0.5, width=0.2, centromere_height=0.2, **kwargs)


class ChromosomeScene(Scene):
    def construct(self):
        # Define a list of colors for chromosomes
        chromosome_colors = [BLUE, RED, GREEN, YELLOW, PURPLE, ORANGE, TEAL, PINK]

        # --- Part 1: The Cell and Nucleus ---
        self.next_section("Cell and Nucleus", skip_animations=False)
        
        # Create the cell circle and its label
        cell_circle = Circle(radius=3, color=WHITE, fill_opacity=0.1)
        cell_label = Text("Cell").next_to(cell_circle, DOWN)
        cell = VGroup(cell_circle, cell_label)

        # Create the nucleus circle and its label, positioned within the cell
        nucleus_circle = Circle(radius=1.5, color=BLUE_E, fill_opacity=0.3)
        nucleus_label = Text("Nucleus").next_to(nucleus_circle, UP)
        nucleus = VGroup(nucleus_circle, nucleus_label)
        nucleus.move_to(cell_circle.get_center())

        # Animate the creation of the cell and nucleus
        self.play(Create(cell_circle), Write(cell_label))
        self.play(Create(nucleus_circle), Write(nucleus_label))
        self.wait(1)

        # Zoom into the nucleus by scaling it up and fading out the cell
        self.play(
            FadeOut(cell_label),
            cell_circle.animate.scale(0.1).fade(1), # Shrink and fade the cell circle
            nucleus.animate.scale(2).center() # Scale up and center the nucleus VGroup
        )
        self.wait(0.5)

        # Update nucleus label position after scaling
        nucleus_label.become(Text("Nucleus").move_to(nucleus_circle.get_center()).shift(UP*1.5))
        self.play(Write(nucleus_label))
        self.wait(1)

        # --- Part 2: Introducing Chromosomes ---
        self.next_section("Introducing Chromosomes", skip_animations=False)
        
        # Create multiple X-shaped chromosomes with random colors
        chromosomes = VGroup()
        num_chromosomes = 6 # Display a subset for clarity
        for i in range(num_chromosomes):
            chrom = XChromosome(color=random.choice(chromosome_colors))
            chromosomes.add(chrom)

        # Arrange chromosomes in a grid and scale them
        chromosomes.arrange_in_grid(rows=2, cols=3, buff=1.0).scale(0.7)
        chromosomes.move_to(ORIGIN)

        # Fade out the nucleus and introduce the chromosomes
        self.play(
            FadeOut(nucleus_label),
            FadeOut(nucleus_circle), 
            LaggedStart(*[Create(chrom) for chrom in chromosomes], lag_ratio=0.2) # Staggered creation
        )
        self.wait(1)

        # Highlight one chromosome and label it
        target_chrom = chromosomes[2]
        chrom_label = Text("Chromosome", font_size=30).next_to(target_chrom, UP, buff=0.5)
        self.play(
            target_chrom.animate.scale(1.2).set_color(YELLOW), # Enlarge and change color
            Write(chrom_label)
        )
        self.wait(1.5)
        self.play(
            target_chrom.animate.scale(1/1.2).set_color(chromosomes[2].get_color()), # Revert to original state
            FadeOut(chrom_label)
        )
        self.wait(0.5)

        # --- Part 3: Chromosome Structure (DNA) ---
        self.next_section("Chromosome Structure (DNA)", skip_animations=False)
        
        # Take a single chromosome to demonstrate its DNA structure
        single_chrom = XChromosome(color=BLUE).scale(1.5).to_edge(LEFT, buff=1)
        chrom_label_dna = Text("Chromosome", font_size=30).next_to(single_chrom, UP, buff=0.5)

        self.play(
            FadeOut(chromosomes), # Fade out the group of chromosomes
            Create(single_chrom),
            Write(chrom_label_dna)
        )
        self.wait(1)

        # Create a DNA double helix mobject
        dna_helix = DNA_DoubleHelix(
            strand_colors=[GREEN_D, GREEN_E],
            height=6,
            width=1.5
        ).to_edge(RIGHT, buff=1)
        dna_label = Text("DNA (Deoxyribonucleic Acid)", font_size=24).next_to(dna_helix, UP, buff=0.5)

        # Animate the conceptual uncoiling of the chromosome into DNA
        self.play(
            FadeOut(chrom_label_dna),
            single_chrom.animate.scale(0.1).fade(1), # Shrink and fade the chromosome
            Create(dna_helix),
            Write(dna_label)
        )
        self.wait(2)

        # Animate the re-coiling of DNA back into a chromosome
        self.play(
            FadeOut(dna_label),
            FadeOut(dna_helix),
            single_chrom.animate.scale(15).set_opacity(1).to_edge(LEFT, buff=1) # Re-appear and scale up
        )
        # Update the chromosome label after its transformation
        chrom_label_dna.become(Text("Chromosome", font_size=30).next_to(single_chrom, UP, buff=0.5))
        self.play(Write(chrom_label_dna))
        self.wait(1)

        # --- Part 4: Genes on Chromosomes ---
        self.next_section("Genes on Chromosomes", skip_animations=False)
        
        # Create rectangles to represent genes on the chromosome arms
        # single_chrom[0] is the first chromatid, [0][0] is its p-arm, [0][1] is its q-arm
        gene1_rect = Rectangle(width=single_chrom[0][0].get_width() * 1.5, height=0.3, color=YELLOW, fill_opacity=0.7)
        gene2_rect = Rectangle(width=single_chrom[0][0].get_width() * 1.5, height=0.3, color=YELLOW, fill_opacity=0.7)

        # Position genes on the p-arm and q-arm of the first chromatid
        gene1_rect.move_to(single_chrom[0][0].get_center()).shift(UP * 0.1) 
        gene2_rect.move_to(single_chrom[0][1].get_center()).shift(DOWN * 0.1) 

        gene_label = Text("Gene", font_size=24).next_to(gene1_rect, RIGHT, buff=0.3)
        gene_label_desc = Text("Instructions for traits", font_size=20).next_to(gene_label, DOWN, buff=0.1)

        # Animate the highlighting of genes and their labels
        self.play(
            Create(gene1_rect),
            Create(gene2_rect),
            Write(gene_label),
            Write(gene_label_desc)
        )
        self.wait(2)

        self.play(
            FadeOut(gene1_rect),
            FadeOut(gene2_rect),
            FadeOut(gene_label),
            FadeOut(gene_label_desc),
            FadeOut(chrom_label_dna)
        )
        self.wait(0.5)

        # --- Part 5: Homologous Chromosomes ---
        self.next_section("Homologous Chromosomes", skip_animations=False)
        
        # Create two homologous chromosomes (one maternal, one paternal)
        homolog_chrom1 = XChromosome(color=BLUE).scale(1.2)
        homolog_chrom2 = XChromosome(color=RED).scale(1.2) 

        # Arrange them side-by-side
        homolog_pair = VGroup(homolog_chrom1, homolog_chrom2).arrange(RIGHT, buff=1.5).center()
        homolog_label = Text("Homologous Chromosomes", font_size=30).next_to(homolog_pair, UP, buff=0.5)
        homolog_desc = Text("One from each parent", font_size=24).next_to(homolog_label, DOWN, buff=0.1)

        self.play(
            FadeOut(single_chrom),
            Create(homolog_pair),
            Write(homolog_label),
            Write(homolog_desc)
        )
        self.wait(2)

        # Show corresponding genes on homologous chromosomes
        gene_homolog1_rect = Rectangle(width=homolog_chrom1[0][0].get_width() * 1.5, height=0.3, color=YELLOW, fill_opacity=0.7)
        gene_homolog2_rect = Rectangle(width=homolog_chrom2[0][0].get_width() * 1.5, height=0.3, color=YELLOW, fill_opacity=0.7)

        gene_homolog1_rect.move_to(homolog_chrom1[0][0].get_center()).shift(UP * 0.1)
        gene_homolog2_rect.move_to(homolog_chrom2[0][0].get_center()).shift(UP * 0.1)

        gene_label_homolog = Text("Same gene, different versions (alleles)", font_size=20).next_to(homolog_pair, DOWN, buff=0.5)

        self.play(
            Create(gene_homolog1_rect),
            Create(gene_homolog2_rect),
            Write(gene_label_homolog)
        )
        self.wait(2)

        self.play(
            FadeOut(gene_homolog1_rect),
            FadeOut(gene_homolog2_rect),
            FadeOut(gene_label_homolog),
            FadeOut(homolog_label),
            FadeOut(homolog_desc)
        )
        self.wait(0.5)

        # --- Part 6: Sex Chromosomes ---
        self.next_section("Sex Chromosomes", skip_animations=False)
        
        # Create X and Y chromosomes for a male (XY)
        x_chrom_male = XChromosome(color=BLUE).scale(1.2)
        y_chrom_male = YChromosome(color=RED).scale(1.2) # Y is visually distinct (shorter)

        male_pair = VGroup(x_chrom_male, y_chrom_male).arrange(RIGHT, buff=1.5).to_edge(UP, buff=1)
        male_label = Text("Male (XY)", font_size=30).next_to(male_pair, UP, buff=0.5)

        # Create two X chromosomes for a female (XX)
        x_chrom_female1 = XChromosome(color=BLUE).scale(1.2)
        x_chrom_female2 = XChromosome(color=RED).scale(1.2)

        female_pair = VGroup(x_chrom_female1, x_chrom_female2).arrange(RIGHT, buff=1.5).to_edge(DOWN, buff=1)
        female_label = Text("Female (XX)", font_size=30).next_to(female_pair, DOWN, buff=0.5)

        sex_chrom_title = Text("Sex Chromosomes", font_size=36).to_edge(LEFT, buff=0.5).shift(UP*0.5)

        self.play(
            FadeOut(homolog_pair),
            Write(sex_chrom_title),
            Create(male_pair),
            Write(male_label),
            Create(female_pair),
            Write(female_label)
        )
        self.wait(3)

        self.play(
            FadeOut(sex_chrom_title),
            FadeOut(male_pair),
            FadeOut(male_label),
            FadeOut(female_pair),
            FadeOut(female_label)
        )
        self.wait(1)

        # --- Final Title ---
        self.next_section("Conclusion", skip_animations=False)
        final_title = Text("Chromosomes: The Blueprint of Life", font_size=48, color=GREEN_B)
        self.play(Write(final_title))
        self.wait(2)
        self.play(FadeOut(final_title))
        self.wait(1)