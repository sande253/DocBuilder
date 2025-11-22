from manim import *

class EMC2Animation(Scene):
    def construct(self):
        # 1. Create individual MathTex elements for E=MC
        # These will be used to build the equation step-by-step.
        e = MathTex("E")
        equals = MathTex("=")
        m = MathTex("M")
        c = MathTex("C")
        two = MathTex("2") # The '2' for the exponent

        # 2. Arrange the initial parts of the equation (E=MC)
        # We group them to position them together and make space for the exponent.
        equation_parts_initial = VGroup(e, equals, m, c).arrange(RIGHT, buff=0.5)
        equation_parts_initial.center().shift(LEFT * 2) # Shift left to make space for C^2

        # 3. Animate the appearance of E, =, M, and C
        self.play(
            Write(e),
            Write(equals),
            Write(m),
            Write(c),
            lag_ratio=0.5, # Stagger the appearance slightly
            run_time=2
        )
        self.wait(0.5)

        # 4. Prepare the '2' for the exponent
        two.scale(0.7) # Make the '2' smaller for superscript
        # Position '2' slightly above and to the right of 'C' initially
        two.next_to(c, UP + RIGHT * 0.1, buff=0.05)

        # 5. Animate '2' appearing and moving into its superscript position
        # To get the exact target position for '2' as a superscript,
        # we create a temporary MathTex for "C^2" and extract the '2' part's properties.
        temp_c_squared = MathTex("C^2").move_to(c.get_center())
        target_two_pos = temp_c_squared.get_parts_by_tex("2")[0].get_center()
        target_two_scale = temp_c_squared.get_parts_by_tex("2")[0].get_scale()

        self.play(
            FadeIn(two, shift=UP), # '2' fades in from above
            two.animate.move_to(target_two_pos).scale(target_two_scale / two.get_scale()),
            run_time=1.5
        )
        self.wait(0.5)

        # 6. Create the final complete equation as a single MathTex object
        final_equation = MathTex("E=MC^2")
        # Position the final equation to align with the current arrangement
        # We use the center of the current VGroup of all elements for consistent centering.
        final_equation.move_to(VGroup(e, equals, m, c, two).get_center())

        # 7. Animate the transformation of the individual parts into the final, unified equation
        # TransformMatchingTex is ideal for smoothly morphing text elements.
        self.play(
            TransformMatchingTex(VGroup(e, equals, m, c, two), final_equation),
            run_time=1.5
        )
        self.wait(1)

        # 8. Add a final highlight to emphasize the completed equation
        self.play(
            final_equation.animate.scale(1.1), # Briefly scale up
            Flash(final_equation, flash_radius=0.5, line_length=0.2, num_lines=10, color=YELLOW),
            run_time=0.5
        )
        self.play(final_equation.animate.scale(1/1.1)) # Scale back to original size
        self.wait(2)
