from ghost import Ghost
ghost = Ghost(wait_timeout=999)
result, resources = ghost.wait_for_selector("div='statistics-table-summary'")
print result