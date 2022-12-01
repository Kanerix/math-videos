from manim import *
import math

class NewtonRaphsonIntro(Scene):
	def construct(self):
		x_range=ValueTracker([1, 10, 1])
		axes = always_redraw(lambda: Axes(x_range=x_range.get_value(), y_range=[0,10,1]))
		graph=always_redraw(lambda: axes.plot(lambda x: x**2, color=BLUE))

		self.play(Create(axes), Create(graph))

		self.play(x_range.animate.set([1, 3, 1]))

class NewtonRaphsonUsage(Scene):
	def construct(self):
		func = lambda x: x - math.cos(x)
		func_deriv = lambda x: 1 + math.sin(x)

		axes = Axes(
			x_range=[-2, 10, 1],
			y_range=[-2, 7, 1],
		).scale(0.85)
		axes.to_edge(UL)
		graph = axes.plot(func, color=BLUE)
		self.play(Create(axes))
		self.play(Create(graph))

		self.wait()

		zero_point = Dot(axes.c2p(0.739, 0))
		zero_point_label = MathTex("x")
		zero_point_label.next_to(zero_point, DOWN)

		self.play(Create(zero_point), Write(zero_point_label))

		self.wait()

		starting_number = 6.5
		drawing_queue = []

		for i in range(1):
			graph_dot = Dot(axes.c2p(starting_number, func(starting_number)))
			x_axes_dot = Dot(axes.c2p(starting_number, 0))
			x_axes_label = MathTex(f"x_{i}").next_to(x_axes_dot, DOWN)
			v_line = DashedLine(
				graph_dot.get_bottom(),
				x_axes_dot.get_top(),
				color=RED
			)

			tangent = lambda x: (func_deriv(starting_number) * (x - starting_number) + func(starting_number))
			graph_tangent = axes.plot(tangent, color=GREEN)

			newton_raphsons = lambda x: (x - func(x) / func_deriv(x))
			tangent_x_interceptor = Dot(
				axes.c2p(newton_raphsons(starting_number), 0)
			)
			tangent_x_interceptor_label = MathTex(f"x_{i+1}").next_to(tangent_x_interceptor, DOWN)
			brace = BraceBetweenPoints(
				tangent_x_interceptor.get_bottom(),
				x_axes_dot.get_center(),
				color=YELLOW,
			)

			drawing_queue.append({
				"x_value": newton_raphsons(starting_number),
				"graph_dot": graph_dot,
				"x_axes_dot": x_axes_dot,
				"x_axes_label": x_axes_label,
				"v_line": v_line,
				"graph_tangent": graph_tangent,
				"tangent_x_interceptor": tangent_x_interceptor,
				"tangent_x_interceptor_label": tangent_x_interceptor_label,
				"brace": brace
			})

		self.play(Create(drawing_queue[0]["graph_dot"]))
		self.play(Create(drawing_queue[0]["v_line"]))
		self.play(
			Create(drawing_queue[0]["x_axes_dot"]),
			Write(drawing_queue[0]["x_axes_label"])
		)

		self.wait()

		self.play(Create(drawing_queue[0]["graph_tangent"]))
		self.play(
			Create(drawing_queue[0]["tangent_x_interceptor"]),
			Write(drawing_queue[0]["tangent_x_interceptor_label"])
		)

		self.wait()

		self.play(Create(drawing_queue[0]["brace"]))
		
		self.wait()