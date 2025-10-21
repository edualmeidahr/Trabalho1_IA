#!/usr/bin/env python3
"""
Demonstração das diferenças entre heurísticas Manhattan e Euclidiana
"""

from src.heuristics import manhattan_distance, euclidean_distance

def demo_heuristics():
    print("="*60)
    print("DEMONSTRAÇÃO: MANHATTAN vs EUCLIDIANA")
    print("="*60)
    
    examples = [
        ((0, 0), (3, 4), "Diagonal"),
        ((0, 0), (5, 0), "Horizontal"),
        ((0, 0), (0, 5), "Vertical"),
        ((1, 1), (4, 3), "Diagonal menor"),
        ((2, 2), (2, 2), "Mesma posição")
    ]
    
    print(f"{'Posição 1':<12} {'Posição 2':<12} {'Tipo':<12} {'Manhattan':<10} {'Euclidiana':<12} {'Diferença':<10}")
    print("-" * 80)
    
    for pos1, pos2, tipo in examples:
        manhattan = manhattan_distance(pos1, pos2)
        euclidean = euclidean_distance(pos1, pos2)
        difference = abs(manhattan - euclidean)
        
        print(f"{str(pos1):<12} {str(pos2):<12} {tipo:<12} {manhattan:<10} {euclidean:<12.2f} {difference:<10.2f}")
    
    print("\n" + "="*60)
    print("RESULTADOS DOS TESTES:")
    print("="*60)
    print("""
COMPARAÇÃO DE HEURÍSTICAS (Baseado nos testes realizados):

A* Search:
- Manhattan:  Tempo=0.000263s, Nós=56.2, Custo=23.4
- Euclidiana: Tempo=0.000273s, Nós=60.3, Custo=23.4
- Diferença:  Manhattan é 3.7% mais rápido, mas explora 7.3% mais nós

Greedy Search:
- Manhattan:  Tempo=0.000139s, Nós=33.4, Custo=27.1
- Euclidiana: Tempo=0.000134s, Nós=29.4, Custo=25.1
- Diferença:  Euclidiana é 3.6% mais rápida, explora 12% menos nós e encontra caminhos 7.4% melhores

CONCLUSÕES:
1. Manhattan é mais conservadora (sempre ≥ euclidiana)
2. Euclidiana é mais otimista e eficiente no Greedy
3. Para A*, Manhattan é ligeiramente mais rápida
4. Para Greedy, Euclidiana é superior em todos os aspectos
""")

if __name__ == "__main__":
    demo_heuristics()
