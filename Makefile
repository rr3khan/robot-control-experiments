# Makefile for Robot Control Experiments

.PHONY: help build start stop clean test docs lint

help:
	@echo "Robot Control Experiments - Makefile Commands"
	@echo "=============================================="
	@echo "  build       - Build Docker containers"
	@echo "  start       - Start Docker containers"
	@echo "  stop        - Stop Docker containers"
	@echo "  shell       - Open shell in ROS2 container"
	@echo "  build-ros   - Build ROS2 workspace"
	@echo "  clean       - Clean build artifacts and logs"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linters"
	@echo "  demo        - Run quick demo"

build:
	docker-compose build

start:
	docker-compose up -d
	@echo "Containers started. Use 'make shell' to enter."

stop:
	docker-compose down

shell:
	docker-compose exec ros2 bash

build-ros:
	docker-compose exec ros2 bash -c "cd /workspace && ./scripts/build_ros.sh"

clean:
	rm -rf ros2_ws/build ros2_ws/install ros2_ws/log
	rm -f logs/*.csv
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

test:
	docker-compose exec ros2 bash -c "cd /workspace/ros2_ws && colcon test && colcon test-result --verbose"

lint:
	@echo "Running Python linters..."
	docker-compose exec ros2 bash -c "cd /workspace && python3 -m flake8 python_controllers analysis --max-line-length=120"

demo:
	@echo "Starting quick demo..."
	docker-compose exec -d ros2 bash -c "source /workspace/ros2_ws/install/setup.bash && ros2 run robot_simulation diff_drive_sim"
	@sleep 3
	docker-compose exec ros2 bash -c "source /workspace/ros2_ws/install/setup.bash && python3 /workspace/scripts/quick_demo.py"

logs:
	docker-compose logs -f

restart: stop start
