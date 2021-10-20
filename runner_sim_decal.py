import logging
from pydantic import Field
from pathlib import Path

from ROAR.utilities_module.data_structures_models import Location, Rotation
from ROAR_Sim.configurations.configuration import Configuration as CarlaConfig
from ROAR_Sim.carla_client.carla_runner import CarlaRunner
from ROAR.agent_module.pure_pursuit_agent import PurePursuitAgent
from ROAR.configurations.configuration import Configuration as AgentConfig
from ROAR.agent_module.michael_pid_agent import PIDAgent
# added this to show the demo in lecture 2
from ROAR.agent_module.occu_map_demo_driving_agent import OccuMapDemoDrivingAgent
from ROAR.agent_module.potential_field_agent import PotentialFieldAgent

def main():
    """Starts game loop"""
    agent_config = AgentConfig.parse_file(Path("./ROAR_Sim/configurations/agent_configuration.json"))
    agent_config2 = AgentConfig.parse_file(Path("./ROAR_Sim/configurations/agent_configuration2.json"))
    carla_config = CarlaConfig.parse_file(Path("./ROAR_Sim/configurations/configuration.json"))

    carla_runner = CarlaRunner(carla_settings=carla_config,
                               agent_settings=agent_config,
                               npc_agent_class=PurePursuitAgent)
    try:
        my_vehicle = carla_runner.set_carla_world()
        agent = PIDAgent(vehicle=my_vehicle, agent_settings=agent_config)
        print("HELLO-----")
        agent.init_cam()
        intrinsic_matrix_front_rgb_camera = agent.front_rgb_camera.intrinsics_matrix
        print("\n intrinsic_matrix_front_rgb_camera \n")
        print(intrinsic_matrix_front_rgb_camera)
        print("\n")

        print("part two")
        # agent.front_rgb_camera.transform.location(10, 5, 20)
        # agent.front_rgb_camera.transform.rotation(20, 30, 0)
        # p2 = agent.front_rgb_camera.transform.get_matrix()
        agent2 = PIDAgent(vehicle=my_vehicle, agent_settings=agent_config2)
        # agent2.front_rgb_camera.transform.location = Field(Location(x=10, y=5, z=20))
        # assume this is what they meant because in the instructions that changed the order and put yaw twice??
        # agent2.front_rgb_camera.transform.rotation = Field(Rotation(pitch=20, yaw=30, roll=0))
        p2 = agent2.front_depth_camera.transform.get_matrix()
        print("\n extrinsic matrix q2 -- p2 on front_depth_camera \n")
        print(p2)
        print("\n")
        carla_runner.start_game_loop(agent=agent, use_manual_control=False)
    except Exception as e:
        logging.error(f"Something bad happened during initialization: {e}")
        carla_runner.on_finish()
        logging.error(f"{e}. Might be a good idea to restart Server")


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(name)s '
                               '- %(message)s',
                        datefmt="%H:%M:%S",
                        level=logging.DEBUG)
    import warnings

    warnings.filterwarnings("ignore", module="carla")
    main()
