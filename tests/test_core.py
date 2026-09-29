import unittest

import core


class TestCore(unittest.TestCase):
    def test_01_no_duplicate_feed(self):
        state = core.new_game()
        self.assertTrue(core.feed(state, 1, 10))
        self.assertFalse(core.feed(state, 1, 10))

    def test_02_machine_capacity(self):
        state = core.new_game()
        state["machine_load"] = 2
        result = core.feed(state, 2, 1)
        self.assertFalse(result)

    def test_03_moisture_boundary(self):
        state = core.new_game()
        self.assertEqual(core.check_moisture(state, 40), "wet")

    def test_04_cancel_releases(self):
        state = core.new_game()
        core.feed(state, 1, 10)
        core.cancel(state, 1)
        self.assertEqual(state["machine_load"], 0)

    def test_05_no_produce_on_fault(self):
        state = core.new_game()
        state["whitewater_fault"] = True
        result = core.produce(state, 5)
        self.assertFalse(result)

    def test_06_break_once(self):
        state = core.new_game()
        core.break_event(state)
        self.assertEqual(state["loss"], 10)

    def test_07_no_start_without_pulp(self):
        state = core.new_game()
        state["pulp"] = 0
        result = core.start(state)
        self.assertFalse(result)

    def test_08_load_preserves_batch(self):
        state = core.new_game()
        state["batch_id"] = 4
        loaded = core.load_state(core.save_state(state))
        self.assertEqual(loaded["batch_id"], 4)


if __name__ == "__main__":
    unittest.main()
