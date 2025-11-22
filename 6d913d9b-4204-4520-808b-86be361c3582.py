from manim import *

class EMC2Explanation(Scene):
    def construct(self):
        # Helper function to create a VGroup of a Rectangle and centered Text
        # All text elements (equation components, explanations) will use this structure.
        def create_labeled_box(text_str, scale_factor=1.0, color=WHITE, rect_fill_opacity=0.2, rect_stroke_opacity=1.0):
            text = Text(text_str).scale(scale_factor).set_color(color)
            # Add some padding to the rectangle around the text
            rect = Rectangle(
                width=text.width + 0.6,
                height=text.height + 0.6,
                color=BLUE_GREY,
                fill_opacity=rect_fill_opacity,
                stroke_opacity=rect_stroke_opacity
            ).move_to(text)
            return VGroup(rect, text)

        # 1. Introduce the E=mc^2 equation
        # Create VGroups for each component of the equation
        e_obj = create_labeled_box("E")
        eq_obj = create_labeled_box("=")
        m_obj = create_labeled_box("m")

        # Create 'c' and '2' as separate VGroups to allow individual highlighting
        c_group = create_labeled_box("c")
        # For the superscript '2', make its bounding box more subtle
        sq_group = create_labeled_box("2", scale_factor=0.7, rect_fill_opacity=0.1, rect_stroke_opacity=0.5)

        # Position '2' as a superscript relative to 'c_group's text element
        # c_group.submobjects[1] is the Text("c") object within the c_group VGroup
        sq_group.next_to(c_group.submobjects[1], UP + RIGHT * 0.1, buff=0.05)
        
        # Combine c_group and sq_group into a single VGroup for 'c^2'
        # This ensures they move together and are treated as one unit during arrangement
        c_squared_combined = VGroup(c_group, sq_group)

        # Arrange the full equation elements horizontally
        equation_elements = VGroup(e_obj, eq_obj, m_obj, c_squared_combined).arrange(RIGHT, buff=0.4)
        
        self.play(Write(equation_elements)) # Animate writing the equation
        self.wait(1)

        # Shift the entire equation up to make space for explanations below
        self.play(equation_elements.animate.shift(UP * 2))
        self.wait(0.5)

        # 2. Explain 'E' (Energy)
        e_explanation = create_labeled_box("Energy", scale_factor=0.8, color=YELLOW)
        e_explanation.next_to(e_obj, DOWN, buff=0.8) # Position explanation below 'E'
        
        self.play(
            e_obj.animate.set_color(YELLOW), # Highlight 'E' by changing its color
            FadeIn(e_explanation) # Fade in the explanation for 'E'
        )
        self.wait(2)
        self.play(
            e_obj.animate.set_color(WHITE), # Revert 'E' color
            FadeOut(e_explanation) # Fade out the explanation
        )
        self.wait(0.5)

        # 3. Explain 'm' (Mass)
        m_explanation = create_labeled_box("Mass", scale_factor=0.8, color=YELLOW)
        m_explanation.next_to(m_obj, DOWN, buff=0.8) # Position explanation below 'm'

        self.play(
            m_obj.animate.set_color(YELLOW), # Highlight 'm'
            FadeIn(m_explanation)
        )
        self.wait(2)
        self.play(
            m_obj.animate.set_color(WHITE), # Revert 'm' color
            FadeOut(m_explanation)
        )
        self.wait(0.5)

        # 4. Explain 'c' (Speed of Light)
        # Highlight only the 'c' part of 'c^2'
        c_explanation = create_labeled_box("Speed of Light", scale_factor=0.8, color=YELLOW)
        c_explanation.next_to(c_group, DOWN, buff=0.8) # Position explanation below 'c'

        self.play(
            c_group.animate.set_color(YELLOW), # Highlight 'c'
            FadeIn(c_explanation)
        )
        self.wait(2)
        self.play(
            c_group.animate.set_color(WHITE), # Revert 'c' color
            FadeOut(c_explanation)
        )
        self.wait(0.5)

        # 5. Explain 'c^2' (Speed of Light Squared)
        c_sq_explanation = create_labeled_box("c² means c multiplied by itself", scale_factor=0.7, color=YELLOW)
        # Position explanation below the combined c^2 part
        c_sq_explanation.next_to(c_squared_combined, DOWN, buff=0.8)

        self.play(
            c_group.animate.set_color(YELLOW), # Highlight 'c'
            sq_group.animate.set_color(YELLOW), # Highlight '2'
            FadeIn(c_sq_explanation)
        )
        self.wait(3)
        self.play(
            c_group.animate.set_color(WHITE), # Revert 'c' color
            sq_group.animate.set_color(WHITE), # Revert '2' color
            FadeOut(c_sq_explanation)
        )
        self.wait(0.5)

        # 6. Summary of the equation
        summary_text_str = "Energy is equal to mass multiplied by the speed of light squared."
        summary_explanation = create_labeled_box(summary_text_str, scale_factor=0.7, color=GREEN)
        summary_explanation.next_to(equation_elements, DOWN, buff=1.0) # Position summary below the equation

        self.play(FadeIn(summary_explanation))
        self.wait(4)
        self.play(FadeOut(summary_explanation), FadeOut(equation_elements)) # Fade out all elements
        self.wait(1)
