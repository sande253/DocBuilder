from manim import *

class PartialFractions(Scene):
    def construct(self):
        # 1. Introduction: Display the original rational function
        title = Text("Partial Fraction Decomposition", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        original_function_tex = MathTex(
            r"F(x) = \frac{5x - 7}{x^2 - 2x - 3}"
        ).next_to(title, DOWN, buff=0.8)
        self.play(FadeIn(original_function_tex))
        self.wait(1)

        # 2. Goal: State the goal
        goal_text = Text("Goal: Decompose into simpler fractions", font_size=36).next_to(original_function_tex, DOWN, buff=0.8)
        self.play(Write(goal_text))
        self.wait(1)

        self.play(FadeOut(goal_text))

        # 3. Factor Denominator
        step1_title = Text("Step 1: Factor the Denominator", font_size=36).next_to(original_function_tex, DOWN, buff=0.8)
        self.play(Write(step1_title))
        self.wait(0.5)

        denominator_original = MathTex(r"x^2 - 2x - 3").next_to(step1_title, DOWN, buff=0.5)
        self.play(Write(denominator_original))
        self.wait(0.5)

        denominator_factored = MathTex(r"(x - 3)(x + 1)").next_to(denominator_original, RIGHT, buff=0.5)
        arrow = MathTex(r"\Rightarrow").next_to(denominator_original, RIGHT, buff=0.2)
        self.play(
            Transform(denominator_original, denominator_factored),
            FadeIn(arrow)
        )
        self.wait(1)

        # Update the original function with factored denominator
        original_function_factored_den = MathTex(
            r"F(x) = \frac{5x - 7}{(x - 3)(x + 1)}"
        ).move_to(original_function_tex.get_center())
        self.play(
            Transform(original_function_tex, original_function_factored_den),
            FadeOut(step1_title, denominator_original, arrow)
        )
        self.wait(1)

        # 4. Set up Partial Fractions with A and B as VGroups
        step2_title = Text("Step 2: Set up the Partial Fractions", font_size=36).next_to(original_function_tex, DOWN, buff=0.8)
        self.play(Write(step2_title))
        self.wait(0.5)

        # Create A and B as VGroups (Rectangle + Text)
        A_tex = MathTex("A")
        A_rect = Rectangle(color=BLUE).surround(A_tex, buff=0.1)
        A_element = VGroup(A_rect, A_tex)

        B_tex = MathTex("B")
        B_rect = Rectangle(color=GREEN).surround(B_tex, buff=0.1)
        B_element = VGroup(B_rect, B_tex)

        # Construct the first fraction: A / (x-3)
        frac1_num = A_element
        frac1_den_tex = MathTex(r"x - 3")
        frac1_line = Line(LEFT, RIGHT)
        frac1 = VGroup(frac1_num, frac1_line, frac1_den_tex).arrange(DOWN, buff=0.1)
        frac1_line.set_width(max(frac1_num.width, frac1_den_tex.width) * 1.1)
        frac1_num.next_to(frac1_line, UP, buff=0.1)
        frac1_den_tex.next_to(frac1_line, DOWN, buff=0.1)

        # Construct the second fraction: B / (x+1)
        frac2_num = B_element
        frac2_den_tex = MathTex(r"x + 1")
        frac2_line = Line(LEFT, RIGHT)
        frac2 = VGroup(frac2_num, frac2_line, frac2_den_tex).arrange(DOWN, buff=0.1)
        frac2_line.set_width(max(frac2_num.width, frac2_den_tex.width) * 1.1)
        frac2_num.next_to(frac2_line, UP, buff=0.1)
        frac2_den_tex.next_to(frac2_line, DOWN, buff=0.1)

        # Assemble the full partial fraction setup equation
        eq_lhs = original_function_tex.copy() # Use the factored form from before
        eq_equals = MathTex(r"=")
        eq_plus = MathTex(r"+")

        partial_fraction_setup_vgroup = VGroup(
            eq_lhs, eq_equals, frac1, eq_plus, frac2
        ).arrange(RIGHT, buff=0.4).next_to(step2_title, DOWN, buff=0.5)

        self.play(Transform(original_function_tex, eq_lhs))
        self.play(Write(VGroup(eq_equals, frac1, eq_plus, frac2)))
        self.wait(2)

        self.play(FadeOut(step2_title))

        # 5. Combine RHS and Equate Numerators
        step3_title = Text("Step 3: Equate Numerators", font_size=36).next_to(partial_fraction_setup_vgroup, UP, buff=0.8)
        self.play(Write(step3_title))
        self.wait(0.5)

        # Create components for the equated numerators equation
        eq_num_lhs = MathTex(r"5x - 7")
        eq_num_equals = MathTex(r"=")
        
        # A(x+1) term (using a copy of A_element)
        term_A_paren = MathTex(r"(x + 1)")
        term_A_vgroup = VGroup(A_element.copy(), term_A_paren).arrange(RIGHT, buff=0.1)

        # B(x-3) term (using a copy of B_element)
        term_B_paren = MathTex(r"(x - 3)")
        term_B_vgroup = VGroup(B_element.copy(), term_B_paren).arrange(RIGHT, buff=0.1)

        eq_num_plus = MathTex(r"+")

        equated_numerators_vgroup = VGroup(
            eq_num_lhs, eq_num_equals, term_A_vgroup, eq_num_plus, term_B_vgroup
        ).arrange(RIGHT, buff=0.4).move_to(partial_fraction_setup_vgroup.get_center())

        self.play(
            Transform(partial_fraction_setup_vgroup, equated_numerators_vgroup)
        )
        self.wait(2)

        self.play(FadeOut(step3_title))

        # 6. Solve for Constants (Method 1: Substitution)
        step4_title = Text("Step 4: Solve for A and B (Substitution Method)", font_size=36).next_to(equated_numerators_vgroup, UP, buff=0.8)
        self.play(Write(step4_title))
        self.wait(0.5)

        # Solve for A (let x = 3)
        sub_x3_text = MathTex(r"\text{Let } x = 3:").next_to(equated_numerators_vgroup, DOWN, buff=0.5).align_to(equated_numerators_vgroup, LEFT)
        self.play(Write(sub_x3_text))
        self.wait(0.5)

        calc_A_line1 = MathTex(r"5(3) - 7 = A(3 + 1) + B(3 - 3)").next_to(sub_x3_text, DOWN, buff=0.3).align_to(sub_x3_text, LEFT)
        self.play(Write(calc_A_line1))
        self.wait(0.5)

        calc_A_line2 = MathTex(r"15 - 7 = 4A + 0").next_to(calc_A_line1, DOWN, buff=0.3).align_to(calc_A_line1, LEFT)
        self.play(Transform(calc_A_line1, calc_A_line2))
        self.wait(0.5)

        calc_A_line3 = MathTex(r"8 = 4A").next_to(calc_A_line1, DOWN, buff=0.3).align_to(calc_A_line1, LEFT)
        self.play(Transform(calc_A_line1, calc_A_line3))
        self.wait(0.5)

        A_value_tex = MathTex(r"A = 2").next_to(calc_A_line1, DOWN, buff=0.3).align_to(calc_A_line1, LEFT)
        self.play(Transform(calc_A_line1, A_value_tex))
        self.wait(1)

        # Solve for B (let x = -1)
        sub_x_neg1_text = MathTex(r"\text{Let } x = -1:").next_to(A_value_tex, DOWN, buff=0.5).align_to(A_value_tex, LEFT)
        self.play(Write(sub_x_neg1_text))
        self.wait(0.5)

        calc_B_line1 = MathTex(r"5(-1) - 7 = A(-1 + 1) + B(-1 - 3)").next_to(sub_x_neg1_text, DOWN, buff=0.3).align_to(sub_x_neg1_text, LEFT)
        self.play(Write(calc_B_line1))
        self.wait(0.5)

        calc_B_line2 = MathTex(r"-5 - 7 = 0 - 4B").next_to(calc_B_line1, DOWN, buff=0.3).align_to(calc_B_line1, LEFT)
        self.play(Transform(calc_B_line1, calc_B_line2))
        self.wait(0.5)

        calc_B_line3 = MathTex(r"-12 = -4B").next_to(calc_B_line1, DOWN, buff=0.3).align_to(calc_B_line1, LEFT)
        self.play(Transform(calc_B_line1, calc_B_line3))
        self.wait(0.5)

        B_value_tex = MathTex(r"B = 3").next_to(calc_B_line1, DOWN, buff=0.3).align_to(calc_B_line1, LEFT)
        self.play(Transform(calc_B_line1, B_value_tex))
        self.wait(1)

        # Clear intermediate calculations
        self.play(
            FadeOut(step4_title, sub_x3_text, A_value_tex, sub_x_neg1_text, B_value_tex),
            FadeOut(equated_numerators_vgroup) # Fade out the equation we just solved
        )
        self.wait(0.5)

        # 7. Substitute Constants Back into A_element and B_element
        step5_title = Text("Step 5: Substitute A and B back", font_size=36).next_to(title, DOWN, buff=0.8)
        self.play(Write(step5_title))
        self.wait(0.5)

        # Create the final A and B elements with their values
        A_final_tex = MathTex("2")
        A_final_rect = Rectangle(color=BLUE).surround(A_final_tex, buff=0.1)
        A_final_element = VGroup(A_final_rect, A_final_tex).move_to(A_element.get_center()) # Position where A_element was

        B_final_tex = MathTex("3")
        B_final_rect = Rectangle(color=GREEN).surround(B_final_tex, buff=0.1)
        B_final_element = VGroup(B_final_rect, B_final_tex).move_to(B_element.get_center()) # Position where B_element was

        # Animate the update of A and B
        self.play(
            Transform(A_element, A_final_element),
            Transform(B_element, B_final_element)
        )
        self.wait(1)

        # Reconstruct the final decomposition using the updated A_element and B_element
        final_frac1_num = A_element # A_element now holds the value '2'
        final_frac1_den_tex = MathTex(r"x - 3")
        final_frac1_line = Line(LEFT, RIGHT)
        final_frac1 = VGroup(final_frac1_num, final_frac1_line, final_frac1_den_tex).arrange(DOWN, buff=0.1)
        final_frac1_line.set_width(max(final_frac1_num.width, final_frac1_den_tex.width) * 1.1)
        final_frac1_num.next_to(final_frac1_line, UP, buff=0.1)
        final_frac1_den_tex.next_to(final_frac1_line, DOWN, buff=0.1)

        final_frac2_num = B_element # B_element now holds the value '3'
        final_frac2_den_tex = MathTex(r"x + 1")
        final_frac2_line = Line(LEFT, RIGHT)
        final_frac2 = VGroup(final_frac2_num, final_frac2_line, final_frac2_den_tex).arrange(DOWN, buff=0.1)
        final_frac2_line.set_width(max(final_frac2_num.width, final_frac2_den_tex.width) * 1.1)
        final_frac2_num.next_to(final_frac2_line, UP, buff=0.1)
        final_frac2_den_tex.next_to(final_frac2_line, DOWN, buff=0.1)

        final_decomposition_vgroup = VGroup(
            final_frac1, MathTex(r"+"), final_frac2
        ).arrange(RIGHT, buff=0.4).next_to(step5_title, DOWN, buff=0.5)

        self.play(Write(final_decomposition_vgroup))
        self.wait(2)

        # 8. Final Result
        final_result_text = Text("Final Decomposition:", font_size=40).next_to(title, DOWN, buff=0.8)
        self.play(
            Transform(step5_title, final_result_text)
        )
        self.wait(0.5)

        original_function_final = MathTex(
            r"\frac{5x - 7}{x^2 - 2x - 3}"
        ).next_to(final_result_text, DOWN, buff=0.5)
        equals_sign = MathTex(r"=").next_to(original_function_final, RIGHT, buff=0.3)
        
        # Position the final decomposition next to the equals sign
        final_decomposition_display = final_decomposition_vgroup.copy().next_to(equals_sign, RIGHT, buff=0.3)

        self.play(
            Write(original_function_final),
            Write(equals_sign),
            Transform(final_decomposition_vgroup, final_decomposition_display) # Transform the previous result to its final position
        )
        self.wait(3)

        self.play(
            FadeOut(title, final_result_text, original_function_final, equals_sign, final_decomposition_display)
        )
        self.wait(1)
