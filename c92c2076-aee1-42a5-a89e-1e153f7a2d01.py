import manim
from manim import *

class ChromosomeVisualization(Scene):
    def construct(self):
        # --- Configuration --- 
        # Define dimensions for chromosome and gene elements for consistent scaling
        chromosome_width = 0.5
        chromosome_height = 3.0 # Total height of the two arms combined, excluding buff
        arm_height = (chromosome_height - 0.1) / 2 # 0.1 is the buff between arms for centromere effect
        gene_height = 0.4
        gene_width = chromosome_width * 0.8

        # --- Helper Functions/Classes ---
        # Custom VGroup for a Chromosome, encapsulating its shape and label
        class Chromosome(VGroup):
            def __init__(self, number, color=BLUE, **kwargs):
                super().__init__(**kwargs)
                
                # Create the top arm of the chromosome
                arm_top = RoundedRectangle(
                    corner_radius=0.1,
                    width=chromosome_width,
                    height=arm_height,
                    color=color,
                    fill_opacity=0.8
                )
                # Create the bottom arm of the chromosome
                arm_bottom = RoundedRectangle(
                    corner_radius=0.1,
                    width=chromosome_width,
                    height=arm_height,
                    color=color,
                    fill_opacity=0.8
                )
                
                # Arrange arms to form the chromosome body with a small gap for centromere
                self.chromosome_body = VGroup(arm_top, arm_bottom).arrange(direction=DOWN, buff=0.1)
                self.add(self.chromosome_body)

                # Create and position the chromosome number label
                self.number_label = Text(f"Chr {number}", font_size=24, color=WHITE)
                self.number_label.next_to(self.chromosome_body, UP, buff=0.2)
                self.add(self.number_label)
                
                self.color = color # Store color for potential gene creation with matching shades

            # Method to add a gene (as a VGroup) to the chromosome
            def add_gene(self, gene_name, relative_y_pos, gene_color=GREEN):
                # relative_y_pos: float from -0.5 (top of chromosome_body) to 0.5 (bottom of chromosome_body)
                # where 0 is the center of the chromosome_body VGroup.
                
                # Create the rectangle representing the gene
                gene_rect = Rectangle(
                    width=gene_width,
                    height=gene_height,
                    color=gene_color,
                    fill_opacity=0.9
                )
                # Create the text label for the gene
                gene_text = Text(gene_name, font_size=18, color=BLACK)
                # Group the rectangle and text together
                gene_vgroup = VGroup(gene_rect, gene_text)
                # Center the text within the gene rectangle
                gene_text.move_to(gene_rect.get_center())

                # Calculate target y-position relative to the chromosome_body's center
                target_y = self.chromosome_body.get_center()[1] + relative_y_pos * (self.chromosome_body.height / 2)
                
                # Move the gene VGroup to the calculated y-position
                gene_vgroup.move_to(self.chromosome_body.get_center())
                gene_vgroup.set_y(target_y)

                # Add the gene VGroup to the main Chromosome VGroup so it moves with the chromosome
                self.add(gene_vgroup)
                return gene_vgroup

        # --- Scene Start ---
        # Display the main title of the animation
        title = Text("How Chromosomes Work", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # --- Part 1: What is a Chromosome? ---
        # Display subtitle for the first section
        part1_title = Text("1. What is a Chromosome?", font_size=36).next_to(title, DOWN, buff=0.8).to_edge(LEFT)
        self.play(Write(part1_title))
        self.wait(0.5)

        # Create and display a single chromosome
        chromosome1 = Chromosome(number=1, color=BLUE).scale(0.8)
        chromosome1.next_to(part1_title, RIGHT, buff=1.5)
        
        # Add text explaining chromosome composition
        dna_text = Text("Tightly packed DNA", font_size=24, color=YELLOW).next_to(chromosome1, DOWN, buff=0.5)
        
        self.play(Create(chromosome1))
        self.play(FadeIn(dna_text, shift=UP))
        self.wait(2)

        # --- Part 2: Homologous Chromosomes ---
        # Fade out previous elements and display new subtitle
        self.play(FadeOut(part1_title, shift=LEFT), FadeOut(dna_text, shift=DOWN))
        
        part2_title = Text("2. Homologous Chromosomes", font_size=36).next_to(title, DOWN, buff=0.8).to_edge(LEFT)
        self.play(Write(part2_title))
        self.wait(0.5)

        # Create a homologous chromosome (similar but slightly different shade)
        chromosome1_homolog = Chromosome(number=1, color=BLUE_D).scale(0.8)
        
        # Create a temporary VGroup to calculate target positions for arrangement
        temp_pair_target = VGroup(chromosome1.copy(), chromosome1_homolog.copy()).arrange(RIGHT, buff=0.8).move_to(ORIGIN)

        # Animate the existing chromosome moving to its new position and creating the homolog
        self.play(
            chromosome1.animate.move_to(temp_pair_target[0].get_center()),
            Create(chromosome1_homolog.move_to(temp_pair_target[1].get_center()))
        )
        # Group the actual chromosome objects for future manipulations
        homologous_pair = VGroup(chromosome1, chromosome1_homolog)
        self.wait(1)

        # Explain homologous chromosomes
        homolog_text = Text("Pairs of chromosomes (one from each parent)", font_size=24, color=YELLOW).next_to(homologous_pair, DOWN, buff=0.5)
        self.play(FadeIn(homolog_text, shift=UP))
        self.wait(2)

        # --- Part 3: Genes on Chromosomes ---
        # Fade out previous elements and display new subtitle
        self.play(FadeOut(part2_title, shift=LEFT), FadeOut(homolog_text, shift=DOWN))

        part3_title = Text("3. Genes on Chromosomes", font_size=36).next_to(title, DOWN, buff=0.8).to_edge(LEFT)
        self.play(Write(part3_title))
        self.wait(0.5)

        # Move the homologous pair up to make space for gene labels
        self.play(homologous_pair.animate.shift(UP * 1.5))

        # Add genes to the first chromosome
        gene_a_chr1 = chromosome1.add_gene("Gene A", -0.3, gene_color=GREEN) # Top arm position
        gene_b_chr1 = chromosome1.add_gene("Gene B", 0.3, gene_color=RED)   # Bottom arm position

        self.play(Create(gene_a_chr1), Create(gene_b_chr1))
        self.wait(0.5)

        # Add corresponding genes to the homologous chromosome
        gene_a_chr1_homolog = chromosome1_homolog.add_gene("Gene A", -0.3, gene_color=GREEN_D) # Top arm position
        gene_b_chr1_homolog = chromosome1_homolog.add_gene("Gene B", 0.3, gene_color=RED_D)   # Bottom arm position

        self.play(Create(gene_a_chr1_homolog), Create(gene_b_chr1_homolog))
        self.wait(1)

        # Explain what genes are
        gene_explanation = Text("Segments of DNA that code for traits", font_size=24, color=YELLOW).next_to(homologous_pair, DOWN, buff=0.5)
        self.play(FadeIn(gene_explanation, shift=UP))
        self.wait(2)

        # Highlight corresponding genes on the homologous pair
        self.play(Indicate(gene_a_chr1), Indicate(gene_a_chr1_homolog))
        self.wait(0.5)
        self.play(Indicate(gene_b_chr1), Indicate(gene_b_chr1_homolog))
        self.wait(2)

        # --- Part 4: Karyotype (Simplified) ---
        # Fade out previous elements and display new subtitle
        self.play(FadeOut(part3_title, shift=LEFT), FadeOut(gene_explanation, shift=DOWN))
        self.play(FadeOut(homologous_pair, shift=UP)) # Clear the previous chromosomes

        part4_title = Text("4. Karyotype: The Full Set", font_size=36).next_to(title, DOWN, buff=0.8).to_edge(LEFT)
        self.play(Write(part4_title))
        self.wait(0.5)

        # Create multiple homologous pairs to represent a simplified karyotype
        karyotype_chromosomes = VGroup()
        colors = [BLUE, GREEN, RED, YELLOW, PURPLE, ORANGE] # Cycle through colors for variety

        for i in range(1, 5): # Show 4 pairs for simplicity
            chr_color = colors[(i-1) % len(colors)]
            chr_a = Chromosome(number=i, color=chr_color).scale(0.6)
            chr_b = Chromosome(number=i, color=Color(chr_color).darken(0.5)).scale(0.6)
            pair = VGroup(chr_a, chr_b).arrange(RIGHT, buff=0.3)
            karyotype_chromosomes.add(pair)
        
        # Arrange the pairs in a grid layout
        karyotype_chromosomes.arrange_in_grid(rows=2, cols=2, buff=(1.0, 0.8))
        karyotype_chromosomes.move_to(ORIGIN)

        self.play(Create(karyotype_chromosomes), lag_ratio=0.5) # Animate creation with a slight delay between pairs
        self.wait(1)

        # Explain what a karyotype is
        karyotype_text = Text("Organized display of an organism's chromosomes", font_size=24, color=YELLOW).next_to(karyotype_chromosomes, DOWN, buff=0.5)
        human_karyotype_note = Text("Humans have 23 pairs (46 chromosomes)", font_size=20, color=GRAY).next_to(karyotype_text, DOWN, buff=0.2)

        self.play(FadeIn(karyotype_text, shift=UP))
        self.play(FadeIn(human_karyotype_note, shift=UP))
        self.wait(3)

        # --- End Scene ---
        # Fade out all remaining mobjects to clear the scene
        self.play(FadeOut(VGroup(*self.mobjects)))
        self.wait(1)
