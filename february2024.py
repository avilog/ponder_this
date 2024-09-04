import numpy as np
from sympy import symbols, solve, primerange
from sklearn.model_selection import ParameterGrid
from collections import Counter

def find_num_combs_sum_range(num_lists, ranges):
    """
    :param num_lists:
    :param ranges:
    :return: Total number of combinations for prime, non prime even and non prime not even
    """

    param_grid = {"%d%d" % (r[0], r[1]): range(r[0], r[1] + 1) for r in ranges}
    comb_sums = Counter()
    print("Num combs %d" % len(list(ParameterGrid(param_grid))))
    for combs in list(ParameterGrid(param_grid)):
        total_sum = sum(combs.values())
        comb_sums[total_sum] += 1

    # Counting the outcomes which result in prime sums
    list_sum_outcomes = []
    for num_list in num_lists:
        list_sum_outcomes += [sum(comb_sums[n] for n in num_list)]

    return list_sum_outcomes


def get_prob_round():
    """
    :return: Probabilities for winning one round for Bob and Alice for prime/not primes dice outcome sums
    """
    dice_values = [(1, 4), (1, 6), (1, 8), (0, 9), (1, 12),
                   (1, 20)]  # 6 dice, each with values between first to second number
    max_sum = sum([r[1] for r in dice_values])

    primes_list = list(primerange(2, max_sum + 1))  # Between minimum to max prime
    non_prime_even_list = [n for n in range(1, max_sum + 1) if (n not in primes_list) and (n % 2 == 0)]
    non_prime_not_even_list = [n for n in range(1, max_sum + 1) if (n not in primes_list) and (n % 2 == 1)]

    total_prime_comb, total_non_prime_even_comb, total_non_prime_not_even_comb = find_num_combs_sum_range(
        [primes_list,
         non_prime_even_list,
         non_prime_not_even_list],
        dice_values)

    print(
        f"Num non prime not even {len(non_prime_not_even_list)} Total non prime not even combs {total_non_prime_not_even_comb}")
    print(f"Num non prime even {len(non_prime_even_list)} Total non prime even combs {total_non_prime_even_comb}")
    print(f"Num prime {len(primes_list)} Total prime combs {total_prime_comb}")
    total_combs = np.prod([r[1] - r[0] + 1 for r in dice_values])
    print(f"Total combs by prod {total_combs}")

    # Alice wins if the result is a prime number, and Bob wins if the result is a nonprime even number. Otherwise, the result of the round is a draw.
    prob_alice_wins = total_prime_comb / total_combs  # Probability prime - Alice wins
    prob_not_prime_even = total_non_prime_even_comb / total_combs  # Probability not prime even - Bob wins

    return prob_alice_wins, prob_not_prime_even


def solve_alice_bob_game(prob_alice, prob_bob, num_rounds_players):
    """
    :param prob_alice: Probability that Alice wins a round
    :param prob_bob: Probability that Bob wins a round
    :param num_rounds_players: Required number of consecutive wins
    :return: Probability that Alice wins the game
    """
    print(f"Prob Alice wins round {prob_alice} Prob Bob wins round {prob_bob} num_rounds_players {num_rounds_players}")

    prob_draw = 1 - (prob_alice + prob_bob)
    s1 = symbols('s1')
    vars_a = [s1] + [symbols('a' + str(i + 1)) for i in range(num_rounds_players - 1)]
    vars_b = [symbols('b' + str(i + 1)) for i in range(0, num_rounds_players - 1)]
    eqs = []

    for i in range(num_rounds_players):
        if i < num_rounds_players - 1:
            eqs += [prob_alice * vars_a[i + 1] + prob_bob * vars_b[0] + prob_draw * s1 - vars_a[i]]
        else:
            eqs += [prob_alice + prob_bob * vars_b[0] + prob_draw * s1 - vars_a[i]]

    for i in range(num_rounds_players - 1):

        if i < num_rounds_players - 2:
            eqs += [prob_alice * vars_a[1] + prob_bob * vars_b[i + 1] + prob_draw * s1 - vars_b[i]]
        else:
            eqs += [prob_alice * vars_a[1] + prob_draw * s1 - vars_b[i]]

    print("Num equations %d" % len(eqs))

    sol = solve(eqs)
    return sol[s1]  # Prob Alice wins the game


def test_get_prob_round():
    prob_round_alice, prob_round_bob = get_prob_round()
    assert prob_round_alice == 0.24826171875
    assert prob_round_bob == 0.5


def test_solve_alice_bob_game():
    prob_round_alice, prob_round_bob = 0.24826171875, 0.5
    prob_alice_wins_game = solve_alice_bob_game(prob_round_alice, prob_round_bob, 13)  # first part of the questions
    assert prob_alice_wins_game == 0.0001675666801570852  # Answer for the puzzle
    # Bonus part of the question. now bob wins if its not prime odd
    prob_alice_wins_game = solve_alice_bob_game(prob_round_alice, 1 - (prob_round_alice + prob_round_bob), 300)
    print(prob_alice_wins_game)
    assert prob_alice_wins_game == 0.0152575329367943  # Answer for the bonus
