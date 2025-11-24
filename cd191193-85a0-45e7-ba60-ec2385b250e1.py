import manim

class BubbleSort(manim.Scene):
    def construct(self):
        # Initial array values for the Bubble Sort visualization
        initial_array = [4, 2, 7, 1, 3]
        n = len(initial_array)

        # Create VGroups for each array element. Each VGroup contains a Rectangle and a Text.
        # These VGroups are stored in a list to allow easy access and swapping.
        array_mobjects = []
        for val in initial_array:
            rect = manim.Rectangle(width=1.0, height=1.0, color=manim.BLUE, fill_opacity=0.8)
            text = manim.Text(str(val)).move_to(rect.get_center())
            element_vg = manim.VGroup(rect, text)
            array_mobjects.append(element_vg)

        # Arrange the initial array elements horizontally with consistent spacing.
        # The VGroup(*array_mobjects) creates a single VGroup from all individual element VGroups.
        array_container = manim.VGroup(*array_mobjects).arrange(manim.RIGHT, buff=0.7)
        self.play(manim.Create(array_container)) # Animate the creation of the array elements
        self.wait(1)

        # Add a title for the algorithm at the top of the scene.
        title = manim.Text("Bubble Sort").to_edge(manim.UP)
        self.play(manim.Write(title)) # Animate writing the title
        self.wait(0.5)

        # Bubble Sort Algorithm Visualization
        for i in range(n - 1): # Outer loop for passes
            # Display the current pass number
            pass_label = manim.Text(f"Pass {i + 1}").next_to(title, manim.DOWN)
            self.play(manim.FadeIn(pass_label)) # Animate the appearance of the pass label
            self.wait(0.5)

            for j in range(n - 1 - i): # Inner loop for comparisons in the current pass
                # Get the two adjacent VGroup elements to compare
                m1 = array_mobjects[j]
                m2 = array_mobjects[j + 1]

                # Extract numerical values from the Text objects within the VGroups
                val1 = int(m1[1].text)
                val2 = int(m2[1].text)

                # Highlight elements being compared by changing their rectangle color to YELLOW
                self.play(
                    m1[0].animate.set_color(manim.YELLOW),
                    m2[0].animate.set_color(manim.YELLOW),
                    run_time=0.5
                )
                self.wait(0.5)

                if val1 > val2: # If elements are out of order, perform a swap
                    # Store the current positions of the two VGroups
                    pos1 = m1.get_center()
                    pos2 = m2.get_center()

                    # Animate the movement of the entire VGroups to their new positions
                    self.play(
                        m1.animate.move_to(pos2),
                        m2.animate.move_to(pos1),
                        run_time=1.0
                    )

                    # Update the array_mobjects list to reflect the logical swap
                    array_mobjects[j], array_mobjects[j + 1] = array_mobjects[j + 1], array_mobjects[j]
                    self.wait(0.5)

                # Unhighlight elements after comparison/swap by reverting their rectangle color to BLUE
                # Note: m1 and m2 still refer to the original VGroup objects, whose positions might have changed.
                self.play(
                    m1[0].animate.set_color(manim.BLUE),
                    m2[0].animate.set_color(manim.BLUE),
                    run_time=0.5
                )
                self.wait(0.2)
            
            # After each pass, the largest unsorted element is in its correct sorted position.
            # Mark this element as sorted by changing its rectangle color to GREEN.
            sorted_element_rect = array_mobjects[n - 1 - i][0]
            self.play(sorted_element_rect.animate.set_color(manim.GREEN), run_time=0.7)
            self.wait(0.5)
            self.play(manim.FadeOut(pass_label)) # Remove the pass label before the next pass

        # After all passes, the first element (at index 0) will also be sorted.
        # Mark it green to indicate the entire array is sorted.
        self.play(array_mobjects[0][0].animate.set_color(manim.GREEN), run_time=0.7)
        self.wait(1)

        # Display a final message indicating the completion of the sort.
        final_text = manim.Text("Bubble Sort Complete!").next_to(array_container, manim.DOWN, buff=1.0)
        self.play(manim.Write(final_text)) # Animate writing the final message
        self.wait(2)
        self.play(manim.FadeOut(self.mobjects)) # Clear all mobjects from the scene