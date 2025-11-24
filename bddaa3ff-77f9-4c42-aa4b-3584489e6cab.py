from manim import *

class BubbleSort(Scene):
    def construct(self):
        # 1. Introduction and Initial Array Setup
        title = Text("Bubble Sort Visualization").to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        initial_array_values = [4, 2, 7, 1, 3]
        array_elements = self.create_array_mobjects(initial_array_values)
        # Arrange elements horizontally and center them on the screen
        array_group = VGroup(*array_elements).arrange(RIGHT, buff=0.8).move_to(ORIGIN)
        self.play(FadeIn(array_group))
        self.wait(1)

        # 2. Algorithm Explanation
        explanation_text = Text(
            "Bubble Sort repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.",
            font_size=28
        ).next_to(array_group, DOWN, buff=1)
        self.play(Write(explanation_text))
        self.wait(3)
        self.play(FadeOut(explanation_text))

        # 3. Sorting Process
        self.bubble_sort_animation(array_elements)

        # 4. Time Complexity
        complexity_text = Text("Time Complexity:").next_to(array_group, DOWN, buff=1)
        complexity_formula = MathTex(r"O(n^2)").next_to(complexity_text, RIGHT)
        self.play(Write(complexity_text), Write(complexity_formula))
        self.wait(2)

        # 5. Final State
        final_text = Text("Array Sorted!").next_to(array_group, DOWN, buff=1)
        self.play(FadeOut(complexity_text, complexity_formula), Write(final_text))
        self.wait(2)
        self.play(FadeOut(title, array_group, final_text))

    def create_array_mobjects(self, values):
        elements = []
        for val in values:
            # Create a rectangle for the array element
            rect = Rectangle(width=1.0, height=1.0, color=BLUE_C, fill_opacity=0.8)
            # Create text for the value, centered in the rectangle
            text = Text(str(val), color=BLACK).move_to(rect.get_center())
            # Group the rectangle and text together
            element_vgroup = VGroup(rect, text)
            elements.append(element_vgroup)
        return elements

    def bubble_sort_animation(self, array_mobjects):
        n = len(array_mobjects)
        # Create a mutable list of current integer values for comparison logic
        current_array_values = [int(mobj[1].text) for mobj in array_mobjects]

        # Outer loop for passes
        for i in range(n - 1):
            # Label for the current pass
            pass_label = Text(f"Pass {i + 1}", font_size=30).to_edge(UP).shift(RIGHT * 4)
            self.play(Write(pass_label))
            self.wait(0.5)

            # Inner loop for comparisons within the pass
            for j in range(n - 1 - i):
                # Get the two VGroups to be compared
                mobj1 = array_mobjects[j]
                mobj2 = array_mobjects[j + 1]

                # Highlight elements being compared (change rectangle color)
                self.play(
                    mobj1[0].animate.set_color(YELLOW),
                    mobj2[0].animate.set_color(YELLOW),
                    run_time=0.7
                )
                self.wait(0.3)

                # Get the actual integer values for comparison
                val1 = current_array_values[j]
                val2 = current_array_values[j + 1]

                if val1 > val2:
                    # Animate the swap of the entire VGroups
                    # Store current positions before animation
                    pos1 = mobj1.get_center()
                    pos2 = mobj2.get_center()

                    self.play(
                        mobj1.animate.move_to(pos2),
                        mobj2.animate.move_to(pos1),
                        run_time=1
                    )
                    # Update the list of Mobjects to reflect the new visual order
                    array_mobjects[j], array_mobjects[j + 1] = array_mobjects[j + 1], array_mobjects[j]
                    # Update the list of integer values for correct comparison in next iteration
                    current_array_values[j], current_array_values[j + 1] = current_array_values[j + 1], current_array_values[j]

                # Revert highlight color after comparison/swap
                self.play(
                    mobj1[0].animate.set_color(BLUE_C),
                    mobj2[0].animate.set_color(BLUE_C),
                    run_time=0.7
                )
                self.wait(0.3)

            # After each pass, the largest unsorted element is in its correct place.
            # Mark this sorted element with a different color.
            sorted_element = array_mobjects[n - 1 - i]
            self.play(sorted_element[0].animate.set_color(GREEN_C))
            self.wait(0.5)
            self.play(FadeOut(pass_label)) # Remove pass label after each pass

        # After all passes, the first element (index 0) will also be sorted.
        self.play(array_mobjects[0][0].animate.set_color(GREEN_C))
        self.wait(1)
