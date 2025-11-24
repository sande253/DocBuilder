import manim

class ChromosomeUnit(manim.VGroup):
    def __init__(self, chromosome_id="X", color=manim.BLUE, gene_labels=None, **kwargs):
        super().__init__(**kwargs)

        chromatid_width = 0.3
        chromatid_height = 2.5
        
        # Create two vertical chromatids
        self.chromatid_left = manim.Rectangle(width=chromatid_width, height=chromatid_height, color=color, fill_opacity=0.8)
        self.chromatid_right = manim.Rectangle(width=chromatid_width, height=chromatid_height, color=color, fill_opacity=0.8)
        
        # Position them side-by-side relative to the origin
        self.chromatid_left.next_to(manim.ORIGIN, manim.LEFT, buff=0.1)
        self.chromatid_right.next_to(manim.ORIGIN, manim.RIGHT, buff=0.1)
        
        # Centromere connects the two chromatids
        self.centromere = manim.Circle(radius=0.2, color=manim.WHITE, fill_opacity=1.0).move_to(manim.ORIGIN)
        
        self.add(self.chromatid_left, self.chromatid_right, self.centromere)
        
        self.genes = manim.VGroup()
        # Add genes if labels are provided and there are at least two for top/bottom positions
        if gene_labels and len(gene_labels) >= 2:
            gene_rect_width = chromatid_width * 1.5
            gene_rect_height = 0.3
            gene_buff = 0.2
            
            # Gene 1 (top position on the left chromatid)
            gene1_rect = manim.Rectangle(width=gene_rect_width, height=gene_rect_height, color=manim.YELLOW, fill_opacity=0.7)
            gene1_label = manim.Text(gene_labels[0], font_size=20, color=manim.BLACK)
            self.gene1_vgroup = manim.VGroup(gene1_rect, gene1_label)
            self.gene1_vgroup.move_to(self.chromatid_left.get_top() + manim.DOWN * (gene_rect_height/2 + gene_buff))
            
            # Sister chromatid's copy of Gene 1
            self.gene1_sister_vgroup = self.gene1_vgroup.copy()
            self.gene1_sister_vgroup.move_to(self.chromatid_right.get_top() + manim.DOWN * (gene_rect_height/2 + gene_buff))
            
            # Gene 2 (bottom position on the left chromatid)
            gene2_rect = manim.Rectangle(width=gene_rect_width, height=gene_rect_height, color=manim.GREEN, fill_opacity=0.7)
            gene2_label = manim.Text(gene_labels[1], font_size=20, color=manim.BLACK)
            self.gene2_vgroup = manim.VGroup(gene2_rect, gene2_label)
            self.gene2_vgroup.move_to(self.chromatid_left.get_bottom() + manim.UP * (gene_rect_height/2 + gene_buff))
            
            # Sister chromatid's copy of Gene 2
            self.gene2_sister_vgroup = self.gene2_vgroup.copy()
            self.gene2_sister_vgroup.move_to(self.chromatid_right.get_bottom() + manim.UP * (gene_rect_height/2 + gene_buff))
            
            self.genes.add(self.gene1_vgroup, self.gene1_sister_vgroup, self.gene2_vgroup, self.gene2_sister_vgroup)
            self.add(self.genes)
        
        # Rotate the entire chromosome VGroup to form the characteristic X-shape
        self.rotate(manim.PI/4)
        self.center() # Ensure the entire VGroup is centered after rotation
        
        # Add chromosome number label, positioned relative to the rotated chromosome
        self.chromosome_number_text = manim.Text(f"Chr {chromosome_id}", font_size=24, color=manim.WHITE)
        self.chromosome_number_text.next_to(self, manim.UP, buff=0.3)
        self.add(self.chromosome_number_text)

class ChromosomeExplanation(manim.Scene):
    def construct(self):
        # Scene Title
        title = manim.Text("How Chromosomes Work", font_size=48).to_edge(manim.UP)
        self.play(manim.Write(title))
        self.wait(1)

        # --- Part 1: Single Chromosome Structure ---
        explanation_text1 = manim.Text("1. A Chromosome: Duplicated DNA", font_size=36).next_to(title, manim.DOWN, buff=0.8).to_edge(manim.LEFT)
        self.play(manim.FadeIn(explanation_text1, shift=manim.LEFT))
        self.wait(0.5)

        # Create a single chromosome unit
        chromosome1 = ChromosomeUnit(chromosome_id="1", color=manim.BLUE, gene_labels=["A", "B"])
        chromosome1.scale(0.8).move_to(manim.ORIGIN)
        self.play(manim.Create(chromosome1))
        self.wait(1)

        # Label parts: Chromatid, Centromere, Gene Locus
        chromatid_label = manim.Text("Chromatid", font_size=24, color=manim.WHITE).next_to(chromosome1.chromatid_left, manim.LEFT, buff=0.2)
        centromere_label = manim.Text("Centromere", font_size=24, color=manim.WHITE).next_to(chromosome1.centromere, manim.RIGHT, buff=0.2)
        gene_label_A = manim.Text("Gene Locus (Allele 'A')", font_size=24, color=manim.WHITE).next_to(chromosome1.gene1_vgroup, manim.RIGHT, buff=0.2)
        
        self.play(
            manim.Write(chromatid_label),
            manim.Indicate(chromosome1.chromatid_left),
            manim.Indicate(chromosome1.chromatid_right)
        )
        self.wait(0.5)
        self.play(
            manim.Write(centromere_label),
            manim.Indicate(chromosome1.centromere)
        )
        self.wait(0.5)
        self.play(
            manim.Write(gene_label_A),
            manim.Indicate(chromosome1.gene1_vgroup),
            manim.Indicate(chromosome1.gene1_sister_vgroup)
        )
        self.wait(2)

        # Clear labels for the next part
        self.play(
            manim.FadeOut(chromatid_label, centromere_label, gene_label_A, explanation_text1)
        )
        self.wait(0.5)

        # --- Part 2: Homologous Chromosomes ---
        explanation_text2 = manim.Text("2. Homologous Chromosomes: A Pair", font_size=36).next_to(title, manim.DOWN, buff=0.8).to_edge(manim.LEFT)
        self.play(manim.FadeIn(explanation_text2, shift=manim.LEFT))
        self.wait(0.5)

        # Move chromosome1 to the left to make space for its homolog
        target_pos_chr1 = manim.LEFT * 3
        self.play(chromosome1.animate.move_to(target_pos_chr1))
        self.wait(0.5)

        # Create a homologous chromosome (same ID, different color, different allele for 'A')
        chromosome2 = ChromosomeUnit(chromosome_id="1", color=manim.RED, gene_labels=["a", "B"])
        chromosome2.scale(0.8).move_to(manim.RIGHT * 3)
        self.play(manim.Create(chromosome2))
        self.wait(1)

        # Label them Maternal and Paternal origin
        maternal_label = manim.Text("Maternal", font_size=28, color=manim.BLUE).next_to(chromosome1, manim.DOWN, buff=0.3)
        paternal_label = manim.Text("Paternal", font_size=28, color=manim.RED).next_to(chromosome2, manim.DOWN, buff=0.3)
        
        self.play(manim.Write(maternal_label), manim.Write(paternal_label))
        self.wait(2)

        # --- Part 3: Genes and Alleles ---
        explanation_text3 = manim.Text("3. Genes and Alleles: Variations", font_size=36).next_to(title, manim.DOWN, buff=0.8).to_edge(manim.LEFT)
        self.play(manim.FadeOut(explanation_text2, shift=manim.LEFT), manim.FadeIn(explanation_text3, shift=manim.LEFT))
        self.wait(0.5)

        # Highlight the different alleles for the first gene
        gene_A_label = manim.Text("Allele 'A'", font_size=24, color=manim.YELLOW).next_to(chromosome1.gene1_vgroup, manim.UP, buff=0.1)
        gene_a_label = manim.Text("Allele 'a'", font_size=24, color=manim.YELLOW).next_to(chromosome2.gene1_vgroup, manim.UP, buff=0.1)
        
        self.play(
            manim.Indicate(chromosome1.gene1_vgroup),
            manim.Indicate(chromosome1.gene1_sister_vgroup),
            manim.Write(gene_A_label)
        )
        self.wait(0.5)
        self.play(
            manim.Indicate(chromosome2.gene1_vgroup),
            manim.Indicate(chromosome2.gene1_sister_vgroup),
            manim.Write(gene_a_label)
        )
        self.wait(1)

        allele_definition = manim.Text("Alleles are different versions of the same gene.", font_size=28).next_to(maternal_label, manim.DOWN, buff=0.5).to_edge(manim.LEFT)
        self.play(manim.Write(allele_definition))
        self.wait(2)

        # Highlight the common allele for the second gene
        gene_B_label = manim.Text("Same Allele 'B'", font_size=24, color=manim.GREEN).next_to(chromosome1.gene2_vgroup, manim.DOWN, buff=0.1)
        self.play(
            manim.FadeOut(gene_A_label, gene_a_label),
            manim.Indicate(chromosome1.gene2_vgroup),
            manim.Indicate(chromosome1.gene2_sister_vgroup),
            manim.Indicate(chromosome2.gene2_vgroup),
            manim.Indicate(chromosome2.gene2_sister_vgroup),
            manim.Write(gene_B_label)
        )
        self.wait(2)

        self.play(
            manim.FadeOut(gene_B_label, allele_definition, explanation_text3)
        )
        self.wait(0.5)

        # --- Part 4: Homologous Pairing (Simplified) ---
        explanation_text4 = manim.Text("4. Homologous Pairing (e.g., during Meiosis)", font_size=36).next_to(title, manim.DOWN, buff=0.8).to_edge(manim.LEFT)
        self.play(manim.FadeIn(explanation_text4, shift=manim.LEFT))
        self.wait(0.5)

        # Fade out parental labels before pairing
        self.play(manim.FadeOut(maternal_label, paternal_label))
        
        # Animate homologous chromosomes moving closer to pair
        target_pair_center = manim.ORIGIN
        chr1_target = target_pair_center + manim.LEFT * 0.7
        chr2_target = target_pair_center + manim.RIGHT * 0.7

        self.play(
            chromosome1.animate.move_to(chr1_target),
            chromosome2.animate.move_to(chr2_target),
            run_time=1.5
        )
        self.wait(1)

        pairing_text = manim.Text("Homologous chromosomes pair up.", font_size=28).next_to(chromosome1, manim.DOWN, buff=0.5)
        self.play(manim.Write(pairing_text))
        self.wait(2)

        # Final fade out of all elements
        self.play(
            manim.FadeOut(title, explanation_text4, chromosome1, chromosome2, pairing_text)
        )
        self.wait(1)
