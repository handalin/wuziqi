"""
AI   ---- Black
User ---- White
"""
AI_win = False
USER_win = False
max_depth = 1
L = 15
max_grid_cnt = L * L
max_score = 9999999999
ALPHA     = -9999999999
BETA      = 9999999999
K = L * L / 2
priority_seq = []
for i in range(L / 2 + 1):
  for j in range(K - (L + 1) * i, K - (L - 1) * i + 1):
    priority_seq.append(j)
  for j in range(K - (L - 1) * i + L, K + (L + 1) * i + 1, L):
    priority_seq.append(j)
  for j in range(K - (L + 1) * i + L , K + (L - 1) * i + 1, L):
    priority_seq.append(j)
  for j in range(K + (L - 1) * i + 1, K + (L + 1) * i):
    priority_seq.append(j)


# define the "board situation" = Black_score - White_score

def H(black, white, pos):
  global max_grid_cnt, max_score

  visited = [ [False for i in range(4)] for j in range(L*L) ]
  
  def search(pos, direction, is_Black):
    # search in the given direction
    if is_Black:
      this = black
      that = white
    else:
      this = white
      that = black
    x1 = pos
    x2 = pos
    if direction == 0:
      # vertical
      while x1 >= 0 and x1 in this: 
        visited[x1][direction] = True
        x1 -= L
      y1 = x1
      if x1 >= 0:
        while x1 >= 0 and x1 not in that:
          x1 -= L

      while x2 < max_grid_cnt and x2 in this: 
        visited[x2][direction] = True
        x2 += L
      y2 = x2
      if x2 < max_grid_cnt:
        while x2 < max_grid_cnt and x2 not in that:
          x2 += L
      left_empty = (y1 - x1) / L
      right_empty = (x2 - y2) / L
      contin_cnt = (y2 - y1 - L) / L

    elif direction == 1:
      # horizontal
      while x1 >= 0 and x1 in this: 
        visited[x1][direction] = True
        x1 -= 1
      y1 = x1
      if x1 >= 0:
        while x1 >= 0 and x1 not in that:
          x1 -= 1

      while x2 < max_grid_cnt and x2 in this: 
        visited[x2][direction] = True
        x2 += 1
      y2 = x2
      if x2 < max_grid_cnt:
        while x2 < max_grid_cnt and x2 not in that:
          x2 += 1
      left_empty = y1 - x1
      right_empty = x2 - y2
      contin_cnt = y2 - y1 - 1
    
    elif direction == 2:
      # left up -- right down '\'
      while x1 >= 0 and x1 in this: 
        visited[x1][direction] = True
        x1 -= L + 1
        if (x1 + L + 1) % L == 0:
          break
      y1 = x1
      if x1 >= 0:
        while x1 >= 0 and x1 not in that:
          x1 -= L + 1
          if (x1 + L + 1) % L == 0:
            break

      while x2 < max_grid_cnt and x2 in this:
        visited[x2][direction] = True
        x2 += L + 1
        if (x2 - L - 1) % L == (L - 1):
          break
      y2 = x2
      if x2 < max_grid_cnt:
        while x2 < max_grid_cnt and x2 not in that:
          x2 += L + 1
          if (x2 - L - 1 ) % L == (L - 1):
            break
      left_empty = ( y1 - x1 ) / (L + 1)
      right_empty = ( x2 - y2 ) / (L + 1)
      contin_cnt = (y2 - y1 - L - 1) / (L + 1)

    else:
      # left down -- right up '/'
      while x1 >= 0 and x1 in this: 
        visited[x1][direction] = True
        x1 -= L - 1
        if (x1 + L - 1) % L == (L - 1):
          break
      y1 = x1
      if x1 >= 0:
        while x1 >= 0 and x1 not in that:
          x1 -= L - 1
          if (x1 + L - 1) % L == (L - 1):
            break

      while x2 < max_grid_cnt and x2 in this: 
        visited[x2][direction] = True
        x2 += L - 1
        if (x2 - L + 1) % L == 0:
          break
      y2 = x2
      if x2 < max_grid_cnt:
        while x2 < max_grid_cnt and x2 not in that:
          x2 += L - 1
          if (x2 - L + 1) % L == 0:
            break
      left_empty = ( y1 - x1 ) / (L - 1)
      right_empty = ( x2 - y2 ) / (L - 1)
      contin_cnt = (y2 - y1 - L + 1) / (L - 1)

    # calculate the SCORE!
    """
    ####################################
    ####################################
    this part is the most important part!
    ####################################
    ####################################
    """
    global AI_win, USER_win
    if contin_cnt >= 5:
      if is_Black:
        AI_win = True
      else:
        USER_win = True
      return max_score
    if contin_cnt == 4 and (left_empty or right_empty):
      return max_score * 0.8 
    if contin_cnt == 3 and (left_empty and right_empty):
      return max_score * 0.3
    if not left_empty and not right_empty:
      return 0
    return contin_cnt * min(10, left_empty + contin_cnt + right_empty)

  """
  def get_score(chess_list, is_Black):
    score = 0
    for pos in chess_list:
      # calulate the score of the color given
      for direction in range(4):
        if not visited[pos][direction]:
          visited[pos][direction] = True
          score += search(pos, direction, is_Black)
    return score
  
  black_score = get_score(black, True)
  white_score = get_score(white, False)
  """
  black_score = 0
  white_score = 0
  for i in range(4):
    black_score += search(pos, i, True)
    white_score += search(pos, i, False)
  if white_score >= BETA * 0.75:
    return -white_score
  return black_score - white_score

def dfs(black, white, pos, score, depth, ancestor_value):
  global max_depth, ALPHA, BETA
  ############
  'alpha-beta cutting'
  ############

  if depth >= max_depth:
    return (-1, H(black, white, pos))

  elif depth % 2 == 0:
    # AI play. max-level
    choice = -1
    alpha = ALPHA # very very small
    for i in priority_seq:
      if i not in black and i not in white:
        tem_black = black + [i]
        (pos, tem_score) = dfs(tem_black, white, i, H(tem_black, white, i), depth + 1, alpha)
        if score + tem_score > alpha:
          alpha = score + tem_score
          choice = i
          if alpha >= ancestor_value:
            break
    return (choice, alpha) 
        
  else:
    # user play. min-level
    choice = -1
    beta = BETA # very very big
    for i in priority_seq:
      if i not in black and i not in white:
        tem_white = white + [i]
        (pos, tem_score) = dfs( black, tem_white, i, H(black, tem_white, i), depth + 1, beta)
        if score + tem_score < beta:
          beta = score + tem_score
          choice = i
          if (beta <= ancestor_value):
            break
    return (choice, beta) 


def play(white, black):
  # return the position AI place black chess.
  global AI_win, USER_win
  global max_depth
  # check if the USER win.
  if USER_win:
    return -2333
  ############################################
  if len(white) + len(black) >= 5:
    max_depth = 2
  elif len(white) + len(black) >= 10:
    max_depth = 3
  ############################################
  (pos, score) = dfs(white, black, -1, 0, 0, BETA) 

  # check if the AI win.
  if AI_win:
    return -(pos+1)
  return pos
