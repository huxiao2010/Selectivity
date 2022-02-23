import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

class WeightedHyperCube {
    public int dim;
    public ArrayList<Double> bl, tr;
    public Double area, weight;

    public WeightedHyperCube(int _dim, ArrayList<Double> _bl, ArrayList<Double> _tr, double _weight) {
        dim = _dim;
        bl = _bl;
        tr = _tr;
        weight = _weight;

        area = 1.0;
        for (int i = 0; i < dim; i++){
            if (tr.get(i) < bl.get(i)) {
                area = 0.0;
                break;
            }
            area *= (tr.get(i) - bl.get(i));
        }
    }

    public Double estimate(WeightedHyperCube other) {
        if (dim != other.dim) {
            return 0.0;
        }
        double int_area = 1.0;
        for (int i = 0; i < dim; i++) {
            double le = Math.max(other.bl.get(i), bl.get(i));
            double ri = Math.min(other.tr.get(i), tr.get(i));
            if (le >= ri) {
                return 0.0;
            }
            int_area *= ri - le;
        }
        return int_area / area * weight;
    }
}

class KDTreeNode {
    public WeightedHyperCube whc;
    public int le, ri;

    public KDTreeNode(WeightedHyperCube _whc, int _le, int _ri) {
        whc = _whc;
        le = _le;
        ri = _ri;
    }
}

public class card_est {
    public static String estimator_path = "../model/";
    public static String testset_path = "../../data/HighDim/";
    public static int test_size = 100;
    public static ArrayList<KDTreeNode> nodes = new ArrayList<>();
    private static double epsilon = 1e-12;

    private static ArrayList<WeightedHyperCube> loadWeightedHyperCube(String name, int dim) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader(name));
        String line;

        ArrayList<WeightedHyperCube> whcs = new ArrayList<>();
        while ((line = br.readLine()) != null) {
            String[] data = line.split(",");
            // bl[0], ..., bl[dim - 1], tr[0], ..., tr[dim - 1], weight
            ArrayList<Double> bl = new ArrayList<>();
            ArrayList<Double> tr = new ArrayList<>();
            for (int i = 0; i < dim; i++) {
                bl.add(Double.valueOf(data[i]));
                tr.add(Double.valueOf(data[i + dim]));
            }
            double weight = Double.valueOf(data[2 * dim]);
            whcs.add(new WeightedHyperCube(dim, bl, tr, weight));
        }
        br.close();

        return whcs;
    }

    private static void loadKDTreeNode(String name, int dim) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader(name));
        String line;

        while ((line = br.readLine()) != null) {
            String[] data = line.split(",");
            // bl[0], ..., bl[dim - 1], tr[0], ..., tr[dim - 1], weight
            ArrayList<Double> bl = new ArrayList<>();
            ArrayList<Double> tr = new ArrayList<>();
            for (int i = 0; i < dim; i++) {
                bl.add(Double.valueOf(data[i]));
                tr.add(Double.valueOf(data[i + dim]));
            }
            double weight = Double.valueOf(data[dim * 2]);
            WeightedHyperCube whc = new WeightedHyperCube(dim, bl, tr, weight);
            int le = Integer.valueOf(data[dim * 2 + 1]);
            int ri = Integer.valueOf(data[dim * 2 + 2]);
            nodes.add(new KDTreeNode(whc, le, ri));
        }
        br.close();
    }

    private static int sgn(double x) {
        if (x > epsilon) {
            return 1;
        } else if (x < -epsilon) {
            return -1;
        } else {
            return 0;
        }
    }

    private static double kdtree_estimate(KDTreeNode cur, WeightedHyperCube other) {
        if (cur.le == -1 || cur.ri == -1) {
            boolean in = true;
            for (int i = 0; i < cur.whc.dim; i++) {
                double x = cur.whc.bl.get(i);
                if (x < other.bl.get(i) || x > other.tr.get(i)) {
                    in = false;
                    break;
                }
            }
            if (in) {
                return cur.whc.weight;
            } else {
                return 0.0;
            }
        }
        double area = 1.0;
        for (int i = 0; i < cur.whc.dim; i++) {
            double le = Math.max(cur.whc.bl.get(i), other.bl.get(i));
            double ri = Math.min(cur.whc.tr.get(i), other.tr.get(i));
            if (ri < le) {
                area = 0.0;
                break;
            }
            area *= (ri - le);
        }
        if (sgn(area) == 0) {
            return 0.0;
        } else if (sgn(area - cur.whc.area) == 0) {
            return cur.whc.weight;
        }
        return kdtree_estimate(nodes.get(cur.le), other) + kdtree_estimate(nodes.get(cur.ri), other);
    }

    public static void main(String [] args) throws IOException{
        // java card_est dim estimator testset
        int dim = Integer.parseInt(args[0]);
        String testset_filename = testset_path + args[2] + ".txt";
        String estimator_filename = estimator_path + args[1] + ".txt";
        ArrayList<WeightedHyperCube> testset = loadWeightedHyperCube(testset_filename, dim);

        String query_shape = args[1].split("_")[0];

        if (query_shape.equals("rect") || query_shape.equals("region-tree")) {
            ArrayList<WeightedHyperCube> estimator = loadWeightedHyperCube(estimator_filename, dim);

            long start_time = System.nanoTime();
            double rms_error = 0.0;
            for (int i = testset.size() - test_size - 1; i < testset.size() - 1; i++) {
                WeightedHyperCube test = testset.get(i);
                double est_sel = 0.0;
                for (int j = 0; j < estimator.size(); j++) {
                    WeightedHyperCube est = estimator.get(j);
                    est_sel += est.estimate(test);
                }
                rms_error += Math.pow(est_sel - test.weight, 2);
            }
            System.out.println(String.format("RMS Error : %.3f", Math.sqrt(rms_error / test_size)));
            long end_time = System.nanoTime();
            System.out.println(String.format("Est. Time : %.3f", (end_time - start_time) / 1e9));
        } else if (query_shape.equals("hdpoint")) {
            loadKDTreeNode(estimator_filename, dim);

            long start_time = System.nanoTime();
            double rms_error = 0.0;
            for (int i = testset.size() - test_size - 1; i < testset.size() - 1; i++) {
                WeightedHyperCube test = testset.get(i);
                double est_sel = kdtree_estimate(nodes.get(0), test);
                rms_error += Math.pow(est_sel - test.weight, 2);
            }
            System.out.println(String.format("RMS Error : %.3f", Math.sqrt(rms_error / test_size)));
            long end_time = System.nanoTime();
            System.out.println(String.format("Est. Time : %.3f", (end_time - start_time) / 1e9));
        }
    }
}
