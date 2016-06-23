import click
import string

# reading all the words
dictionary_file = open("corncob_lowercase.txt")
words = dictionary_file.read()
words = words.split()


# finding list of next words
def next_words_list(given_word, repeated_words):
    next_words = [given_word]
    repeated_words.append(given_word)
    for i in range(len(given_word)):
        for letter in string.lowercase:
            # replacing a letter in word by each letter in alphabets and checking if it is in dictionary of words
            new_word = given_word[:i] + letter + given_word[i + 1:]
            if new_word in words and new_word not in repeated_words:
                next_words.append(new_word)
                repeated_words.append(new_word)
    return next_words


# list of next words up to the second word
def small_chain(word1, word2):
    actual_result = [[word1, word1]]
    index = 0
    repeated_words = []
    try:
        while word2 not in actual_result[index]:
            # I'm preserving the first word in actual_result for future use, they are used to find the chain
            for word in actual_result[index][1:]:
                next_words = next_words_list(word, repeated_words)
                actual_result.append(next_words)
                if word2 in next_words:
                    return actual_result
            index += 1
    except IndexError:
        # when there is no connection between the two words
        return []


# find the index of the list of next_words in which the word is present
def find_next_word_index(word, chain_words):
    for i in xrange(len(chain_words)):
        if word in chain_words[i]:
            return i


def get_chain(word1, word2):
    chain_words = small_chain(word1, word2)
    # chain_words contains the list of next_words starting from the word1
    if not chain_words:
        return []
    result = [word2]
    chain_words.reverse()
    while chain_words[1:]:
        # my key is first word in chain_words is in chain, starting from the last so I've reversed it and
        # and taking the first element
        first_word = chain_words[0][0]
        result.append(first_word)
        # finding the first word in chain_words starting 1:end
        index = find_next_word_index(first_word, chain_words[1:])
        chain_words = chain_words[index + 1:]
        # so here the first word in first list in chain words is next word
    return result


# checking if the word is present in dictionary of words
def is_word_in_dictionary(word, words):
    if word not in words:
        click.echo("There is no word as " + word)
        return True


@click.command()
@click.argument('word1')
@click.argument('word2')
def smallest_chain(word1, word2):
    # basic test case, lengths of the two strings must be equal
    if len(word1) != len(word2):
        click.echo("Length of Two words must be Equal.")
        return
    global words
    # another test case the two words must be present in the dictionary of words
    if is_word_in_dictionary(word1, words) or is_word_in_dictionary(word2, words):
        return
    # reducing the words to words which are of length of given words
    words = [word for word in words if len(word) == len(word1)]
    # result contains the chain
    result = get_chain(word2, word1)
    if not result:
        click.echo("There is no connection between words.")
        return
    result_string = ""
    for word in result:
        # result in a string format, with connecting symbol
        result_string += word + "->"
    # removing the last connecting symbol
    result_string = result_string[:-2]
    click.echo(result_string)


if __name__ == '__main__':
    smallest_chain()
