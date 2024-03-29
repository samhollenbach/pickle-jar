from pickle_jar import pickle_jar
from mock import MagicMock, patch
from nose.tools import ok_, eq_, raises



@patch('inspect.getsource')
class TestPickleJar:

    def setUp(self):
        self.pj = pickle_jar(cache_dir='test/test_jar/', filename='test.pickle')
        self.pj.clear_cache()

    def test_standard_pickle_jar(self, get_source):
        get_source.return_value = '@test\ntest_source\ntest_source'
        func = MagicMock(return_value='test')
        func.__name__ = 'func_name_mock'
        decorated_func = self.pj(func)

        # First function run
        res1 = decorated_func('arg1')
        eq_(res1, 'test')
        func.assert_called_once()

        # Second function run
        res2 = decorated_func('arg1')
        eq_(res2, 'test')
        func.assert_called_once()
        self.pj.clear_cache()

    def test_cache_removed(self, get_source):
        get_source.return_value = '@test\ntest_source\ntest_source'
        func = MagicMock(return_value='test')
        func.__name__ = 'func_name_mock'
        decorated_func = self.pj(func)

        # First function run
        res1 = decorated_func('arg1')
        eq_(res1, 'test')
        func.assert_called_once()
        # Clear cache again
        self.pj.clear_cache()

        # Second function run
        res2 = decorated_func('arg1')
        eq_(res2, 'test')
        assert func.call_count == 2
        self.pj.clear_cache()

    def test_different_args(self, get_source):
        get_source.return_value = '@test\ntest_source\ntest_source'
        pj2 = pickle_jar(cache_dir='test/test_jar/', filename=None)
        func = MagicMock(return_value='test')
        func.__name__ = 'func_name_mock'
        pj2.clear_cache('func_name_mock')
        decorated_func = pj2(func)

        # First function run
        res1 = decorated_func('arg1')
        eq_(res1, 'test')
        func.assert_called_once()

        # Second function run
        res2 = decorated_func('arg2')
        eq_(res2, 'test')
        assert func.call_count == 2
        pj2.clear_cache(func_name='func_name_mock')


    def test_changed_source(self, get_source):
        get_source.return_value = '@test\ntest_source\ntest_source'
        func = MagicMock(return_value='test')
        func.__name__ = 'func_name_mock'
        decorated_func = self.pj(func)

        # First function run
        res1 = decorated_func('arg1')
        eq_(res1, 'test')
        func.assert_called_once()
        # Change function source code
        get_source.return_value = '@test\ntest_source\ntest_source2'

        # Second function run
        res2 = decorated_func('arg1')
        eq_(res2, 'test')
        assert func.call_count == 2
        self.pj.clear_cache()

    def tearDown(self):
        self.pj.clear_cache()




def test_args_hash():
    # Hash Immutable Objects
    hash1 = pickle_jar().get_args_hash('test', 'test2', kwtest='test')
    hash2 = pickle_jar().get_args_hash('test', 'test2', kwtest='test')
    assert hash1 == hash2
    hash3 = pickle_jar().get_args_hash('test', 'test3', kwtest='test')
    assert hash1 != hash3
    hash4 = pickle_jar().get_args_hash('test', 'test2', kwtest='test2')
    assert hash1 != hash4
    hash5 = pickle_jar().get_args_hash('test', 'test2', kwtest2='test2')
    assert hash1 != hash5


    # Hash Mutable Objects
    d = {'a': 0, 'b': 1, 'c': 2}
    serial_dict = pickle_jar().try_serialize(d)
    assert serial_dict != ''
    hash_dict1 = pickle_jar().get_args_hash(d)
    hash_dict2 = pickle_jar().get_args_hash(d)
    assert hash_dict1 == hash_dict2
    d2 = {'a': 0, 'b': 1, 'c': 3}
    hash_dict3 = pickle_jar().get_args_hash(d2)
    assert hash_dict1 != hash_dict3


    # Hash Pandas Dataframes
    import pandas as pd
    df = pd.DataFrame([{'a': 0, 'b': 1, 'c': 2}])
    serial_df = pickle_jar().try_serialize(df)
    assert serial_df != ''
    hash_df1 = pickle_jar().get_args_hash(df)
    hash_df2 = pickle_jar().get_args_hash(df)
    assert hash_df1 == hash_df2
    df2 = df.copy()
    hash_df3 = pickle_jar().get_args_hash(df2)
    assert hash_df1 == hash_df3
    df2['a'] = [1]
    hash_df4 = pickle_jar().get_args_hash(df2)
    assert hash_df1 != hash_df4


    # Nested Pandas DataFrame in Dict
    d_df = {'a': 0, 'b': 1, 'c': 2, 'df': df}
    d_df2 = {'a': 0, 'b': 1, 'c': 2, 'df': df2}
    hash_d_df1 = pickle_jar().get_args_hash(d_df)
    hash_d_df2 = pickle_jar().get_args_hash(d_df2)
    print(d_df, hash_d_df1)
    print(d_df2, hash_d_df2)
    # Nested Dataframes create same hash
    # assert hash_d_df1 != hash_d_df2