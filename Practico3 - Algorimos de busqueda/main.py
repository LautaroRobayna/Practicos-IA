import gymnasium
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
from ucs_agent import UCSAgent
from a_star_agent import AStarAgent
from model import Model
import time
import traceback

envs = [
    (
        "4x4",
        gymnasium.make(
            "FrozenLake-v1",
            desc=generate_random_map(size=4),
            is_slippery=False,
            render_mode="human",
        ),
    ),
    (
        "8x8",
        gymnasium.make(
            "FrozenLake-v1",
            desc=generate_random_map(size=8),
            is_slippery=False,
        ),
    ),
    (
        "16x16",
        gymnasium.make(
            "FrozenLake-v1",
            desc=generate_random_map(size=16),
            is_slippery=False,
        ),
    ),
]

agents = [
    ("UCS", UCSAgent),
    ("A*", AStarAgent),
]

def find_start_and_goal(env):
    """Encuentra los estados inicial y objetivo en el mapa"""
    desc = env.unwrapped.desc
    nrows, ncols = desc.shape
    
    start_state = None
    goal_state = None
    
    for row in range(nrows):
        for col in range(ncols):
            cell = desc[row, col].decode('utf-8')
            state = row * ncols + col
            
            if cell == 'S':
                start_state = state
            elif cell == 'G':
                goal_state = state
    
    return start_state, goal_state

def run_agent_on_env(agent_name, agent_class, env_name, env):
    try:
        # Crear el agente con placeholders
        agent = agent_class(env, None, None, None)
        
        # Medir tiempo de ejecución
        start_time = time.time()
        reward, steps = agent.run()
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        return {
            'reward': reward,
            'steps': steps,
            'time': execution_time,
            'success': reward > 0
        }
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        traceback.print_exc()
        return None

def main():
    """Ejecutar los agentes con distintos entornos y comparar performance"""
    print("Iniciando comparacion de agentes de busqueda")
    print("=" * 60)

    results = {}

    for env_name, env in envs:
        print(f"\nProbando en ambiente: {env_name}")
        print("-" * 40)

        results[env_name] = {}

        for agent_name, agent_class in agents:
            print(f"  Ejecutando {agent_name}...")

            result = run_agent_on_env(agent_name, agent_class, env_name, env)

            if result:
                results[env_name][agent_name] = result
                status = "Exito" if result['success'] else "Fallo"
                print(f"    {status} - Pasos: {result['steps']}, Tiempo: {result['time']:.3f}s")
            else:
                results[env_name][agent_name] = None

            # Pausa para ver el resultado
            time.sleep(1)

        env.close()

    # Mostrar resumen final
    print("\nRESUMEN DE RESULTADOS")
    print("=" * 60)

    for env_name in results:
        print(f"\n{env_name}:")
        for agent_name in results[env_name]:
            result = results[env_name][agent_name]
            if result:
                status = "OK" if result['success'] else "FALLO"
                print(f"  {agent_name}: {status} - {result['steps']} pasos, {result['time']:.3f}s")
            else:
                print(f"  {agent_name}: ERROR")

    # Comparacion
    print("\n" + "=" * 60)
    print("COMPARACION DE AGENTES")
    print("=" * 60)

    for env_name in results:
        print(f"\n{env_name}:")

        ucs_result = results[env_name].get('UCS')
        astar_result = results[env_name].get('A*')

        if ucs_result and astar_result:
            print(f"  UCS:  {ucs_result['steps']} pasos, {ucs_result['time']:.3f}s")
            print(f"  A*:   {astar_result['steps']} pasos, {astar_result['time']:.3f}s")

            if astar_result['steps'] < ucs_result['steps']:
                print(f"  -> A* es mejor (menos pasos)")
            elif ucs_result['steps'] < astar_result['steps']:
                print(f"  -> UCS es mejor (menos pasos)")
            elif astar_result['time'] < ucs_result['time']:
                print(f"  -> A* es mejor (mismo pasos, menos tiempo)")
            elif ucs_result['time'] < astar_result['time']:
                print(f"  -> UCS es mejor (mismo pasos, menos tiempo)")
            else:
                print(f"  -> Empate")
        else:
            print("  -> No se puede comparar (uno o ambos fallaron)")

if __name__ == "__main__":
    main()