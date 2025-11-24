from manim import *

class Chromosome(VGroup):
    """
    A VGroup representing a chromosome, either as a single chromatid or replicated (X-shape).
    Can include gene markers.
    """
    def __init__(self, color=BLUE, is_replicated=False, genes_data=None, **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.is_replicated = is_replicated
        self.arm_length = 2.0
        self.arm_width = 0.4
        self.centromere_radius = 0.2

        self.arms = VGroup()
        self.centromere_mobject = None
        self.gene_mobjects = VGroup() # Stores VGroups of (gene_rect, gene_text)

        if not is_replicated:
            # Single chromatid
            arm = Rectangle(width=self.arm_width, height=self.arm_length, color=self.color, fill_opacity=0.8)
            self.arms.add(arm)
            self.add(arm)
        else:
            # Replicated chromosome (X-shape)
            # Create two arms rotated to form an X
            arm1 = Rectangle(width=self.arm_width, height=self.arm_length, color=self.color, fill_opacity=0.8).rotate(-PI/4)
            arm2 = Rectangle(width=self.arm_width, height=self.arm_length, color=self.color, fill_opacity=0.8).rotate(PI/4)
            # Create a centromere at the center
            self.centromere_mobject = Circle(radius=self.centromere_radius, color=RED, fill_opacity=0.8).move_to(ORIGIN)
            
            self.arms.add(arm1, arm2)
            # Add all components to the main VGroup
            self.add(arm1, arm2, self.centromere_mobject)
            self.move_to(ORIGIN) # Ensure the entire chromosome is centered initially

        if genes_data:
            for gene_name, position_prop, gene_color in genes_data:
                # Create a VGroup for each gene marker (shape + text)
                gene_rect = Rectangle(width=0.6, height=0.3, color=gene_color, fill_opacity=0.6)
                gene_text = Text(gene_name, font_size=20, color=BLACK).move_to(gene_rect.get_center())
                gene_vgroup = VGroup(gene_rect, gene_text)

                if not is_replicated:
                    # For a single chromatid, place on its single arm
                    target_point = self.arms[0].get_point_from_proportion(position_prop)
                    gene_vgroup.move_to(target_point)
                    self.gene_mobjects.add(gene_vgroup)
                else:
                    # For replicated, place on both arms (sister chromatids)
                    # Arm1 (rotated -PI/4)
                    target_point_arm1 = self.arms[0].get_point_from_proportion(position_prop)
                    gene_vgroup_arm1 = gene_vgroup.copy().move_to(target_point_arm1)
                    self.gene_mobjects.add(gene_vgroup_arm1)

                    # Arm2 (rotated PI/4)
                    target_point_arm2 = self.arms[1].get_point_from_proportion(position_prop)
                    gene_vgroup_arm2 = gene_vgroup.copy().move_to(target_point_arm2)
                    self.gene_mobjects.add(gene_vgroup_arm2)
        
        if self.gene_mobjects:
            self.add(self.gene_mobjects)

class ChromosomeExplanation(Scene):
    def construct(self):
        # Title of the explanation
        title = Text("Understanding Chromosomes", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 1. Introduce a single chromatid
        self.next_section("Single Chromatid")
        single_chromatid = Chromosome(is_replicated=False).shift(LEFT * 3)
        label_single = Text("Chromatid", font_size=28).next_to(single_chromatid, UP, buff=0.5)
        
        self.play(Create(single_chromatid))
        self.play(Write(label_single))
        self.wait(1.5)

        # 2. Show DNA replication to form a replicated chromosome
        self.next_section("DNA Replication")
        # Create the target replicated chromosome at the same position
        replicated_chromosome_target = Chromosome(is_replicated=True).move_to(single_chromatid.get_center())
        label_replicated = Text("Replicated Chromosome", font_size=28).next_to(replicated_chromosome_target, UP, buff=0.5)
        
        # Animate the transformation from single to replicated chromosome
        # After this transform, 'single_chromatid' will be the replicated chromosome on screen.
        self.play(
            Transform(single_chromatid, replicated_chromosome_target),
            Transform(label_single, label_replicated)
        )
        self.wait(1.5)

        # Label the centromere. Reference the centromere from the transformed 'single_chromatid'.
        label_centromere = Text("Centromere", font_size=20, color=RED).next_to(single_chromatid.centromere_mobject, DOWN, buff=0.2)
        self.play(Write(label_centromere))
        self.wait(1.5)

        # Fade out current elements to prepare for the next section
        self.play(FadeOut(single_chromatid), FadeOut(label_single), FadeOut(label_centromere))
        self.wait(0.5)

        # 3. Introduce homologous chromosomes
        self.next_section("Homologous Chromosomes")
        # Create two homologous chromosomes with different colors and gene alleles
        homolog1 = Chromosome(is_replicated=True, color=BLUE, 
                              genes_data=[("A", 0.7, GREEN), ("B", 0.3, ORANGE)])
        homolog2 = Chromosome(is_replicated=True, color=PURPLE, 
                              genes_data=[("a", 0.7, GREEN), ("B", 0.3, ORANGE)])
        
        # Arrange them side by side
        homolog_pair = VGroup(homolog1, homolog2).arrange(RIGHT, buff=1.5).center()
        
        label_homologs = Text("Homologous Chromosomes", font_size=32).next_to(homolog_pair, UP, buff=0.8)
        
        self.play(FadeIn(homolog_pair))
        self.play(Write(label_homologs))
        self.wait(2)

        # 4. Explain Genes and Alleles
        self.next_section("Genes and Alleles")
        gene_label_text = Text("Genes: Segments of DNA that code for traits", font_size=28).to_edge(DOWN).shift(LEFT*2)
        allele_label_text = Text("Alleles: Different versions of a gene", font_size=28).to_edge(DOWN).shift(RIGHT*2)

        self.play(Write(gene_label_text))
        self.wait(1)

        # Highlight gene 'A' on homolog1 (both sister chromatids)
        # gene_mobjects[0] is 'A' on arm1, gene_mobjects[1] is 'A' on arm2
        gene_A_h1_arm1 = homolog1.gene_mobjects[0]
        gene_A_h1_arm2 = homolog1.gene_mobjects[1]
        self.play(Indicate(gene_A_h1_arm1), Indicate(gene_A_h1_arm2))
        self.wait(1)

        self.play(Write(allele_label_text))
        self.wait(1)

        # Highlight gene 'A' on homolog1 and gene 'a' on homolog2 to show alleles
        gene_a_h2_arm1 = homolog2.gene_mobjects[0]
        gene_a_h2_arm2 = homolog2.gene_mobjects[1]
        self.play(
            Indicate(gene_A_h1_arm1), Indicate(gene_A_h1_arm2),
            Indicate(gene_a_h2_arm1), Indicate(gene_a_h2_arm2)
        )
        self.wait(2)

        # Show the 'B' gene as identical on both homologous chromosomes
        gene_B_h1_arm1 = homolog1.gene_mobjects[2]
        gene_B_h1_arm2 = homolog1.gene_mobjects[3]
        gene_B_h2_arm1 = homolog2.gene_mobjects[2]
        gene_B_h2_arm2 = homolog2.gene_mobjects[3]
        
        self.play(
            Indicate(gene_B_h1_arm1), Indicate(gene_B_h1_arm2),
            Indicate(gene_B_h2_arm1), Indicate(gene_B_h2_arm2)
        )
        self.wait(2)

        # Final fade out of all elements
        self.play(
            FadeOut(title),
            FadeOut(homolog_pair),
            FadeOut(label_homologs),
            FadeOut(gene_label_text),
            FadeOut(allele_label_text)
        )
        self.wait(1)