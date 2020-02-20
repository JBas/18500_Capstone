"""

"""
# specifies that cameras can only be at
# locations forming the border of a square
def getCameraLocals(xs, ys):
    side_1 = zip(
        np.zeros(ys.shape[0]),
        ys)
    side_1 = list(side_1)

    side_2 = zip(
        xs,
        np.zeros(xs.shape[0]))
    side_2 = list(side_2)

    side_3 = zip(
        np.full(ys.shape, xs[-1]),
        ys)
    side_3 = list(side_3)

    side_4 = zip(
        xs,
        np.full(xs.shape, ys[-1]))
    side_4 = list(side_4)

    return np.vstack((side_1, side_2, side_3, side_4))

def calcTrapezoidalFOV(options):
    p0  = options["p0"]
    e   = options["e"]
    phi = options["phi"]
    psi = options["psi"]
    t1  = options["t1"]
    t2  = options["t2"]
    T   = options["T"]

    tau = e / np.cos(t2 + psi)
    if ((np.rad2deg(t2 + psi) < 90) or (tau > T)):
        #print("FOV with such conditions does not exist!")
        return None

    h = 1 # h is not defined in the paper, so this is a guess! big sad

    # get trapezoid vertices assuming (x0, y0) == (0, 0) and phi == 0
    trapezoid = np.array([
                         [h*np.tan(psi)],
                         [(h / np.cos(psi))*np.tan(t1/2)],
                         [h*np.tan(psi)],
                         [(h / np.cos(psi))*-np.tan(t1/2)],
                         [h*np.tan(psi + t2)],
                         [(h / np.cos(psi + t2))*np.tan(t1/2)],
                         [h*np.tan(psi + t2)],
                         [(h / np.cos(psi + t2))*-np.tan(t1/2)]
                         ])
    # caculate trapezoid vertex by rotating by phi
    M = np.array([
                 [np.cos(phi), -np.sin(phi), 0, 0, 0, 0, 0, 0],
                 [np.sin(phi), np.cos(phi), 0, 0, 0, 0, 0, 0],
                 [0, 0, np.cos(phi), -np.sin(phi), 0, 0, 0, 0],
                 [0, 0, np.sin(phi), np.cos(phi), 0, 0, 0, 0],
                 [0, 0, 0, 0, np.cos(phi), -np.sin(phi), 0, 0],
                 [0, 0, 0, 0, np.sin(phi), np.cos(phi), 0, 0],
                 [0, 0, 0, 0, 0, 0, np.cos(phi), -np.sin(phi)],
                 [0, 0, 0, 0, 0, 0, np.sin(phi), np.cos(phi)]
                ])

    trapezoid = M @ trapezoid

    # add actual installment information
    trapezoid = trapezoid + np.vstack((p0[0], p0[1], p0[0], p0[1], p0[0], p0[1], p0[0], p0[1]))
    return trapezoid.reshape((4, 2))

def isCellCovered(i, trapezoid, size):
    cell_pos = np.array(i)*size + size/2

    # from stackOverflow, <3:
    bb = mplPath.Path(trapezoid)
    return bb.contains_point(cell_pos)

def setupV(data):
    size = data["size"] 
    pos = data["pos"] 
    phis = data["phis"]
    psis = data["psis"]
    heights = data["heights"]
    types = data["types"]
    tpos = data["tpos"]
    CVR = data["CVR"] 
    
    N_C = data["N_C"]
    N_hD = data["N_hD"]
    N_vD = data["N_vD"]
    N_E = data["N_E"]
    N_A = data["N_A"]
    N_T = data["N_T"]
    
    v = np.zeros((N_T, N_C, N_hD, N_vD, N_E, N_A), dtype=object)
    names = np.zeros((N_T, N_C, N_hD, N_vD, N_E, N_A), dtype=object)
    for k in range(N_T):
        target = tpos[k]
        for i in range(N_C):
            for j in range(N_hD):
                for d in range(N_vD):
                    for e in range(N_E):
                        for t in range(N_A):
                            camera_params = {
                                "p0": pos[i],
                                "e": heights[e],
                                "phi": phis[j],
                                "psi": psis[d],
                                "t1": types[t][0],
                                "t2": types[t][1],
                                "T": types[t][2]
                            }
                            vis_poly = calcTrapezoidalFOV(camera_params)
                            varname = "v(" + str(k) + "_" + str(i) + "_" + str(j) + "_" + str(d) + "_" + str(e) + "_" + str(t) + ")"
                            names[k, i, j, d, e, t] = varname

                            if (vis_poly is None):
                                v[k, i, j, d, e, t] = 0
                                continue

                            varval = isCellCovered(target, vis_poly, size)
                            v[k, i, j, d, e, t] = varval

    return [v, names]


