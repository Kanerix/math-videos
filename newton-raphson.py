from manim import *
import math

#class NewtonRaphsonIntro(Scene):
	#def construct(self):

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

		numbers = [6.5]
		drawing_queue = []

		for i, n in enumerate(numbers):
			graph_dot = Dot(axes.c2p(6, func(6)))
			x_axes_dot = Dot(axes.c2p(6, 0))
			v_line = DashedLine(
				graph_dot.get_bottom(),
				x_axes_dot.get_top(),
				color=RED
			)
			x_axes_label = MathTex(f"x_{i}").next_to(x_axes_dot, DOWN)
			point_tangent = lambda x: func_deriv(6) * (x - 6) + func(6)

			drawing_queue.append({
				"graph_dot": graph_dot,
				"x_axes_dot": x_axes_dot,
				"v_line": v_line,
				"x_axes_label": x_axes_label,
				"point_tangent": point_tangent
			})

		self.play(Create(drawing_queue[0]["graph_dot"]))
		self.play(Create(drawing_queue[0]["v_line"]))
		self.play(
			Create(drawing_queue[0]["x_axes_dot"]),
			Write(drawing_queue[0]["x_axes_label"])
		)

		self.wait()

		tangent = axes.plot(
			drawing_queue[0]["point_tangent"],
			color=GREEN
		)
		self.play(Create(tangent))

		self.wait()

		self.play(axes.animate.set(x_range=[-2, 2, 0.5], y_range=[-2, 2, 0.5]))

		self.wait()

		self.play(Uncreate(tangent))