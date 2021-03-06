"""Tests for module da on Domain Adaptation """

# Author: Remi Flamary <remi.flamary@unice.fr>
#
# License: MIT License

import numpy as np
from numpy.testing.utils import assert_allclose, assert_equal

import ot
from ot.datasets import get_data_classif
from ot.utils import unif


def test_sinkhorn_lpl1_transport_class():
    """test_sinkhorn_transport
    """

    ns = 150
    nt = 200

    Xs, ys = get_data_classif('3gauss', ns)
    Xt, yt = get_data_classif('3gauss2', nt)

    clf = ot.da.SinkhornLpl1Transport()

    # test its computed
    clf.fit(Xs=Xs, ys=ys, Xt=Xt)
    assert hasattr(clf, "cost_")
    assert hasattr(clf, "coupling_")

    # test dimensions of coupling
    assert_equal(clf.cost_.shape, ((Xs.shape[0], Xt.shape[0])))
    assert_equal(clf.coupling_.shape, ((Xs.shape[0], Xt.shape[0])))

    # test margin constraints
    mu_s = unif(ns)
    mu_t = unif(nt)
    assert_allclose(np.sum(clf.coupling_, axis=0), mu_t, rtol=1e-3, atol=1e-3)
    assert_allclose(np.sum(clf.coupling_, axis=1), mu_s, rtol=1e-3, atol=1e-3)

    # test transform
    transp_Xs = clf.transform(Xs=Xs)
    assert_equal(transp_Xs.shape, Xs.shape)

    Xs_new, _ = get_data_classif('3gauss', ns + 1)
    transp_Xs_new = clf.transform(Xs_new)

    # check that the oos method is working
    assert_equal(transp_Xs_new.shape, Xs_new.shape)

    # test inverse transform
    transp_Xt = clf.inverse_transform(Xt=Xt)
    assert_equal(transp_Xt.shape, Xt.shape)

    Xt_new, _ = get_data_classif('3gauss2', nt + 1)
    transp_Xt_new = clf.inverse_transform(Xt=Xt_new)

    # check that the oos method is working
    assert_equal(transp_Xt_new.shape, Xt_new.shape)

    # test fit_transform
    transp_Xs = clf.fit_transform(Xs=Xs, ys=ys, Xt=Xt)
    assert_equal(transp_Xs.shape, Xs.shape)

    # test semi supervised mode
    clf = ot.da.SinkhornLpl1Transport()
    clf.fit(Xs=Xs, ys=ys, Xt=Xt)
    n_unsup = np.sum(clf.cost_)

    # test semi supervised mode
    clf = ot.da.SinkhornLpl1Transport()
    clf.fit(Xs=Xs, ys=ys, Xt=Xt, yt=yt)
    assert_equal(clf.cost_.shape, ((Xs.shape[0], Xt.shape[0])))
    n_semisup = np.sum(clf.cost_)

    assert n_unsup != n_semisup, "semisupervised mode not working"


def test_sinkhorn_l1l2_transport_class():
    """test_sinkhorn_transport
    """

    ns = 150
    nt = 200

    Xs, ys = get_data_classif('3gauss', ns)
    Xt, yt = get_data_classif('3gauss2', nt)

    clf = ot.da.SinkhornL1l2Transport()

    # test its computed
    clf.fit(Xs=Xs, ys=ys, Xt=Xt)
    assert hasattr(clf, "cost_")
    assert hasattr(clf, "coupling_")
    assert hasattr(clf, "log_")

    # test dimensions of coupling
    assert_equal(clf.cost_.shape, ((Xs.shape[0], Xt.shape[0])))
    assert_equal(clf.coupling_.shape, ((Xs.shape[0], Xt.shape[0])))

    # test margin constraints
    mu_s = unif(ns)
    mu_t = unif(nt)
    assert_allclose(np.sum(clf.coupling_, axis=0), mu_t, rtol=1e-3, atol=1e-3)
    assert_allclose(np.sum(clf.coupling_, axis=1), mu_s, rtol=1e-3, atol=1e-3)

    # test transform
    transp_Xs = clf.transform(Xs=Xs)
    assert_equal(transp_Xs.shape, Xs.shape)

    Xs_new, _ = get_data_classif('3gauss', ns + 1)
    transp_Xs_new = clf.transform(Xs_new)

    # check that the oos method is working
    assert_equal(transp_Xs_new.shape, Xs_new.shape)

    # test inverse transform
    transp_Xt = clf.inverse_transform(Xt=Xt)
    assert_equal(transp_Xt.shape, Xt.shape)

    Xt_new, _ = get_data_classif('3gauss2', nt + 1)
    transp_Xt_new = clf.inverse_transform(Xt=Xt_new)

    # check that the oos method is working
    assert_equal(transp_Xt_new.shape, Xt_new.shape)

    # test fit_transform
    transp_Xs = clf.fit_transform(Xs=Xs, ys=ys, Xt=Xt)
    assert_equal(transp_Xs.shape, Xs.shape)

    # test semi supervised mode
    clf = ot.da.SinkhornL1l2Transport()
    clf.fit(Xs=Xs, ys=ys, Xt=Xt)
    n_unsup = np.sum(clf.cost_)

    # test semi supervised mode
    clf = ot.da.SinkhornL1l2Transport()
    clf.fit(Xs=Xs, ys=ys, Xt=Xt, yt=yt)
    assert_equal(clf.cost_.shape, ((Xs.shape[0], Xt.shape[0])))
    n_semisup = np.sum(clf.cost_)

    assert n_unsup != n_semisup, "semisupervised mode not working"

    # check everything runs well with log=True
    clf = ot.da.SinkhornL1l2Transport(log=True)
    clf.fit(Xs=Xs, ys=ys, Xt=Xt)
    assert len(clf.log_.keys()) != 0


def test_sinkhorn_transport_class():
    """test_sinkhorn_transport
    """

    ns = 150
    nt = 200

    Xs, ys = get_data_classif('3gauss', ns)
    Xt, yt = get_data_classif('3gauss2', nt)

    clf = ot.da.SinkhornTransport()

    # test its computed
    clf.fit(Xs=Xs, Xt=Xt)
    assert hasattr(clf, "cost_")
    assert hasattr(clf, "coupling_")
    assert hasattr(clf, "log_")

    # test dimensions of coupling
    assert_equal(clf.cost_.shape, ((Xs.shape[0], Xt.shape[0])))
    assert_equal(clf.coupling_.shape, ((Xs.shape[0], Xt.shape[0])))

    # test margin constraints
    mu_s = unif(ns)
    mu_t = unif(nt)
    assert_allclose(np.sum(clf.coupling_, axis=0), mu_t, rtol=1e-3, atol=1e-3)
    assert_allclose(np.sum(clf.coupling_, axis=1), mu_s, rtol=1e-3, atol=1e-3)

    # test transform
    transp_Xs = clf.transform(Xs=Xs)
    assert_equal(transp_Xs.shape, Xs.shape)

    Xs_new, _ = get_data_classif('3gauss', ns + 1)
    transp_Xs_new = clf.transform(Xs_new)

    # check that the oos method is working
    assert_equal(transp_Xs_new.shape, Xs_new.shape)

    # test inverse transform
    transp_Xt = clf.inverse_transform(Xt=Xt)
    assert_equal(transp_Xt.shape, Xt.shape)

    Xt_new, _ = get_data_classif('3gauss2', nt + 1)
    transp_Xt_new = clf.inverse_transform(Xt=Xt_new)

    # check that the oos method is working
    assert_equal(transp_Xt_new.shape, Xt_new.shape)

    # test fit_transform
    transp_Xs = clf.fit_transform(Xs=Xs, Xt=Xt)
    assert_equal(transp_Xs.shape, Xs.shape)

    # test semi supervised mode
    clf = ot.da.SinkhornTransport()
    clf.fit(Xs=Xs, Xt=Xt)
    n_unsup = np.sum(clf.cost_)

    # test semi supervised mode
    clf = ot.da.SinkhornTransport()
    clf.fit(Xs=Xs, ys=ys, Xt=Xt, yt=yt)
    assert_equal(clf.cost_.shape, ((Xs.shape[0], Xt.shape[0])))
    n_semisup = np.sum(clf.cost_)

    assert n_unsup != n_semisup, "semisupervised mode not working"

    # check everything runs well with log=True
    clf = ot.da.SinkhornTransport(log=True)
    clf.fit(Xs=Xs, ys=ys, Xt=Xt)
    assert len(clf.log_.keys()) != 0


def test_emd_transport_class():
    """test_sinkhorn_transport
    """

    ns = 150
    nt = 200

    Xs, ys = get_data_classif('3gauss', ns)
    Xt, yt = get_data_classif('3gauss2', nt)

    clf = ot.da.EMDTransport()

    # test its computed
    clf.fit(Xs=Xs, Xt=Xt)
    assert hasattr(clf, "cost_")
    assert hasattr(clf, "coupling_")

    # test dimensions of coupling
    assert_equal(clf.cost_.shape, ((Xs.shape[0], Xt.shape[0])))
    assert_equal(clf.coupling_.shape, ((Xs.shape[0], Xt.shape[0])))

    # test margin constraints
    mu_s = unif(ns)
    mu_t = unif(nt)
    assert_allclose(np.sum(clf.coupling_, axis=0), mu_t, rtol=1e-3, atol=1e-3)
    assert_allclose(np.sum(clf.coupling_, axis=1), mu_s, rtol=1e-3, atol=1e-3)

    # test transform
    transp_Xs = clf.transform(Xs=Xs)
    assert_equal(transp_Xs.shape, Xs.shape)

    Xs_new, _ = get_data_classif('3gauss', ns + 1)
    transp_Xs_new = clf.transform(Xs_new)

    # check that the oos method is working
    assert_equal(transp_Xs_new.shape, Xs_new.shape)

    # test inverse transform
    transp_Xt = clf.inverse_transform(Xt=Xt)
    assert_equal(transp_Xt.shape, Xt.shape)

    Xt_new, _ = get_data_classif('3gauss2', nt + 1)
    transp_Xt_new = clf.inverse_transform(Xt=Xt_new)

    # check that the oos method is working
    assert_equal(transp_Xt_new.shape, Xt_new.shape)

    # test fit_transform
    transp_Xs = clf.fit_transform(Xs=Xs, Xt=Xt)
    assert_equal(transp_Xs.shape, Xs.shape)

    # test semi supervised mode
    clf = ot.da.EMDTransport()
    clf.fit(Xs=Xs, Xt=Xt)
    n_unsup = np.sum(clf.cost_)

    # test semi supervised mode
    clf = ot.da.EMDTransport()
    clf.fit(Xs=Xs, ys=ys, Xt=Xt, yt=yt)
    assert_equal(clf.cost_.shape, ((Xs.shape[0], Xt.shape[0])))
    n_semisup = np.sum(clf.cost_)

    assert n_unsup != n_semisup, "semisupervised mode not working"


def test_mapping_transport_class():
    """test_mapping_transport
    """

    ns = 150
    nt = 200

    Xs, ys = get_data_classif('3gauss', ns)
    Xt, yt = get_data_classif('3gauss2', nt)
    Xs_new, _ = get_data_classif('3gauss', ns + 1)

    ##########################################################################
    # kernel == linear mapping tests
    ##########################################################################

    # check computation and dimensions if bias == False
    clf = ot.da.MappingTransport(kernel="linear", bias=False)
    clf.fit(Xs=Xs, Xt=Xt)
    assert hasattr(clf, "coupling_")
    assert hasattr(clf, "mapping_")
    assert hasattr(clf, "log_")

    assert_equal(clf.coupling_.shape, ((Xs.shape[0], Xt.shape[0])))
    assert_equal(clf.mapping_.shape, ((Xs.shape[1], Xt.shape[1])))

    # test margin constraints
    mu_s = unif(ns)
    mu_t = unif(nt)
    assert_allclose(np.sum(clf.coupling_, axis=0), mu_t, rtol=1e-3, atol=1e-3)
    assert_allclose(np.sum(clf.coupling_, axis=1), mu_s, rtol=1e-3, atol=1e-3)

    # test transform
    transp_Xs = clf.transform(Xs=Xs)
    assert_equal(transp_Xs.shape, Xs.shape)

    transp_Xs_new = clf.transform(Xs_new)

    # check that the oos method is working
    assert_equal(transp_Xs_new.shape, Xs_new.shape)

    # check computation and dimensions if bias == True
    clf = ot.da.MappingTransport(kernel="linear", bias=True)
    clf.fit(Xs=Xs, Xt=Xt)
    assert_equal(clf.coupling_.shape, ((Xs.shape[0], Xt.shape[0])))
    assert_equal(clf.mapping_.shape, ((Xs.shape[1] + 1, Xt.shape[1])))

    # test margin constraints
    mu_s = unif(ns)
    mu_t = unif(nt)
    assert_allclose(np.sum(clf.coupling_, axis=0), mu_t, rtol=1e-3, atol=1e-3)
    assert_allclose(np.sum(clf.coupling_, axis=1), mu_s, rtol=1e-3, atol=1e-3)

    # test transform
    transp_Xs = clf.transform(Xs=Xs)
    assert_equal(transp_Xs.shape, Xs.shape)

    transp_Xs_new = clf.transform(Xs_new)

    # check that the oos method is working
    assert_equal(transp_Xs_new.shape, Xs_new.shape)

    ##########################################################################
    # kernel == gaussian mapping tests
    ##########################################################################

    # check computation and dimensions if bias == False
    clf = ot.da.MappingTransport(kernel="gaussian", bias=False)
    clf.fit(Xs=Xs, Xt=Xt)

    assert_equal(clf.coupling_.shape, ((Xs.shape[0], Xt.shape[0])))
    assert_equal(clf.mapping_.shape, ((Xs.shape[0], Xt.shape[1])))

    # test margin constraints
    mu_s = unif(ns)
    mu_t = unif(nt)
    assert_allclose(np.sum(clf.coupling_, axis=0), mu_t, rtol=1e-3, atol=1e-3)
    assert_allclose(np.sum(clf.coupling_, axis=1), mu_s, rtol=1e-3, atol=1e-3)

    # test transform
    transp_Xs = clf.transform(Xs=Xs)
    assert_equal(transp_Xs.shape, Xs.shape)

    transp_Xs_new = clf.transform(Xs_new)

    # check that the oos method is working
    assert_equal(transp_Xs_new.shape, Xs_new.shape)

    # check computation and dimensions if bias == True
    clf = ot.da.MappingTransport(kernel="gaussian", bias=True)
    clf.fit(Xs=Xs, Xt=Xt)
    assert_equal(clf.coupling_.shape, ((Xs.shape[0], Xt.shape[0])))
    assert_equal(clf.mapping_.shape, ((Xs.shape[0] + 1, Xt.shape[1])))

    # test margin constraints
    mu_s = unif(ns)
    mu_t = unif(nt)
    assert_allclose(np.sum(clf.coupling_, axis=0), mu_t, rtol=1e-3, atol=1e-3)
    assert_allclose(np.sum(clf.coupling_, axis=1), mu_s, rtol=1e-3, atol=1e-3)

    # test transform
    transp_Xs = clf.transform(Xs=Xs)
    assert_equal(transp_Xs.shape, Xs.shape)

    transp_Xs_new = clf.transform(Xs_new)

    # check that the oos method is working
    assert_equal(transp_Xs_new.shape, Xs_new.shape)

    # check everything runs well with log=True
    clf = ot.da.MappingTransport(kernel="gaussian", log=True)
    clf.fit(Xs=Xs, Xt=Xt)
    assert len(clf.log_.keys()) != 0


def test_otda():

    n_samples = 150  # nb samples
    np.random.seed(0)

    xs, ys = ot.datasets.get_data_classif('3gauss', n_samples)
    xt, yt = ot.datasets.get_data_classif('3gauss2', n_samples)

    a, b = ot.unif(n_samples), ot.unif(n_samples)

    # LP problem
    da_emd = ot.da.OTDA()     # init class
    da_emd.fit(xs, xt)       # fit distributions
    da_emd.interp()    # interpolation of source samples
    da_emd.predict(xs)    # interpolation of source samples

    np.testing.assert_allclose(a, np.sum(da_emd.G, 1))
    np.testing.assert_allclose(b, np.sum(da_emd.G, 0))

    # sinkhorn regularization
    lambd = 1e-1
    da_entrop = ot.da.OTDA_sinkhorn()
    da_entrop.fit(xs, xt, reg=lambd)
    da_entrop.interp()
    da_entrop.predict(xs)

    np.testing.assert_allclose(a, np.sum(da_entrop.G, 1), rtol=1e-3, atol=1e-3)
    np.testing.assert_allclose(b, np.sum(da_entrop.G, 0), rtol=1e-3, atol=1e-3)

    # non-convex Group lasso regularization
    reg = 1e-1
    eta = 1e0
    da_lpl1 = ot.da.OTDA_lpl1()
    da_lpl1.fit(xs, ys, xt, reg=reg, eta=eta)
    da_lpl1.interp()
    da_lpl1.predict(xs)

    np.testing.assert_allclose(a, np.sum(da_lpl1.G, 1), rtol=1e-3, atol=1e-3)
    np.testing.assert_allclose(b, np.sum(da_lpl1.G, 0), rtol=1e-3, atol=1e-3)

    # True Group lasso regularization
    reg = 1e-1
    eta = 2e0
    da_l1l2 = ot.da.OTDA_l1l2()
    da_l1l2.fit(xs, ys, xt, reg=reg, eta=eta, numItermax=20, verbose=True)
    da_l1l2.interp()
    da_l1l2.predict(xs)

    np.testing.assert_allclose(a, np.sum(da_l1l2.G, 1), rtol=1e-3, atol=1e-3)
    np.testing.assert_allclose(b, np.sum(da_l1l2.G, 0), rtol=1e-3, atol=1e-3)

    # linear mapping
    da_emd = ot.da.OTDA_mapping_linear()     # init class
    da_emd.fit(xs, xt, numItermax=10)       # fit distributions
    da_emd.predict(xs)    # interpolation of source samples

    # nonlinear mapping
    da_emd = ot.da.OTDA_mapping_kernel()     # init class
    da_emd.fit(xs, xt, numItermax=10)       # fit distributions
    da_emd.predict(xs)    # interpolation of source samples


# if __name__ == "__main__":

#     test_sinkhorn_transport_class()
#     test_emd_transport_class()
#     test_sinkhorn_l1l2_transport_class()
#     test_sinkhorn_lpl1_transport_class()
#     test_mapping_transport_class()
