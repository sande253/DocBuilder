from manim import *

class BubbleSortAnimation(Scene):
    def construct(self):
        # --- Configuration --- 
        initial_array = [4, 2, 7, 1, 3]
        square_side = 1.0
        buff_spacing = 0.8

        # --- Title --- 
        title = Text("Bubble Sort Visualization", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # --- Create initial array elements --- 
        # Each element is a VGroup of a Rectangle and a Text, centered within the rectangle.
        array_elements = VGroup()
        for num in initial_array:
            square = Square(side_length=square_side, color=BLUE, fill_opacity=0.8)
            text = Text(str(num), color=BLACK).move_to(square.get_center())
            element_vg = VGroup(square, text)
            array_elements.add(element_vg)

        # Arrange elements horizontally and center them on the screen
        array_elements.arrange(RIGHT, buff=buff_spacing).center()
        self.play(Create(array_elements))
        self.wait(1)

        # --- Prepare for sorting --- 
        # `current_visual_array` holds the Manim VGroup objects, allowing their order to be updated.
        # `current_logical_array` holds the integer values, used for comparison logic.
        current_visual_array = list(array_elements)
        current_logical_array = list(initial_array)
        n = len(current_logical_array)

        # --- Bubble Sort Algorithm Animation --- 
        for i in range(n - 1):
            # Display current pass number
            pass_label = Text(f"Pass {i + 1}", font_size=36).next_to(title, DOWN, buff=0.5)
            self.play(Write(pass_label))
            self.wait(0.5)

            for j in range(n - 1 - i):
                element1_vg = current_visual_array[j]
                element2_vg = current_visual_array[j+1]

                # Highlight elements being compared by changing their square's color to YELLOW
                self.play(
                    element1_vg[0].animate.set_color(YELLOW),
                    element2_vg[0].animate.set_color(YELLOW),
                    run_time=0.7
                )
                self.wait(0.3)

                # Compare and swap if necessary
                if current_logical_array[j] > current_logical_array[j+1]:
                    # Animate the swap of the entire VGroup objects
                    self.play(
                        Swap(element1_vg, element2_vg),
                        run_time=1.2
                    )
                    # Update the Python lists to reflect the new order after the animation
                    current_visual_array[j], current_visual_array[j+1] = current_visual_array[j+1], current_visual_array[j]
                    current_logical_array[j], current_logical_array[j+1] = current_logical_array[j+1], current_logical_array[j]
                    self.wait(0.5)
                else:
                    self.wait(0.5) # Pause briefly even if no swap

                # Reset colors of compared elements to BLUE
                self.play(
                    element1_vg[0].animate.set_color(BLUE),
                    element2_vg[0].animate.set_color(BLUE),
                    run_time=0.7
                )
                self.wait(0.3)

            # After each pass, the largest unsorted element is in its correct place.
            # Mark this element as sorted by changing its square's color to GREEN.
            sorted_element_vg = current_visual_array[n - 1 - i]
            self.play(
                sorted_element_vg[0].animate.set_color(GREEN),
                run_time=0.7
            )
            self.wait(0.5)
            self.play(FadeOut(pass_label)) # Remove pass label for the next pass

        # The first element is also sorted after all passes are complete.
        self.play(
            current_visual_array[0][0].animate.set_color(GREEN),
            run_time=0.7
        )
        self.wait(2)

        # --- Final Fade Out --- 
        self.play(FadeOut(array_elements, title))
        self.wait(1)
