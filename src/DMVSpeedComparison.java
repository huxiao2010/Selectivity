package edu.illinois.quicksel.experiments;

import edu.illinois.quicksel.basic.AssertionReader;
import edu.illinois.quicksel.Assertion;
import edu.illinois.quicksel.Hyperrectangle;
import edu.illinois.quicksel.quicksel.QuickSel;
import edu.illinois.quicksel.isomer.Isomer;
import org.apache.commons.lang3.tuple.Pair;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.Vector;
import java.util.ArrayList;
import java.util.Collections;

public class DMVSpeedComparison {

  public static void main(String[] args) throws IOException {
    List<String> datasets = Arrays.asList("Forest-2d", "Forest-2d-data", "Power-2d", "Power-2d-data");
    List<String> assertions_list = Arrays.asList("forest/assertion_forest_2d.txt", "data_sensitive/forest-data-2100-2d.txt", "power/power-2d-10001.txt", "data_sensitive/power-data-10000-2d.txt");
    List<Double> mix_ratio = Arrays.asList(0.0, 0.25, 0.5, 0.75, 1.0);

    for (int i = 3; i < 4; i++) {
      Pair<Vector<Assertion>, Vector<Assertion>> assertionPair = AssertionReader.readAssertion(assertions_list.get(i), "forest/permanent_assertion_2d.txt");
      Vector<Assertion> assertions = assertionPair.getLeft();
      Vector<Assertion> permanent_assertions = assertionPair.getRight();
      String teststring = String.format("Mixture/%s.txt", datasets.get(i));
      System.out.println("====== " + teststring + "======");

      List<Vector> aa = new ArrayList<Vector>();
      for (int j = 0; j < 5; j++) {
        double ratio = mix_ratio.get(j);
//         String test_name = String.format("Train data: %s Test R: %.2f Test D: %.2f", datasets.get(i), ratio, 1 - ratio);
        String testset = String.format("Mixture/%s_r%.2f_d%.2f.txt", datasets.get(i - (i % 2)), ratio, 1 - ratio);
        Vector<Assertion> queryAssertion = AssertionReader.readAssertion(testset).getLeft();
        aa.add(queryAssertion);

//         System.out.println("====== " + test_name + "======");

//         System.out.println("QuickSel test");

//         System.out.println("");


//         System.out.println("Isomer test");
//         isomerTest(permanent_assertions, assertions, queryAssertion);
//         System.out.println("");
      }
      quickSelTest(permanent_assertions, assertions, aa);
    }
// data_sensitive/forest-data-2100-2d
  }

  private static void quickSelTest(
      Vector<Assertion> permanent_assertions,
      Vector<Assertion> assertions,
      List<Vector> aa) {

    // build Crumbs
    List<Integer> list = Arrays.asList(
        2000);
    List<Integer> pointers = Arrays.asList(50,
        95,
        99,
        100);
    for (int assertionNum : list) {
      Pair<Hyperrectangle, Double> range_freq = computeMinMaxRange();
      QuickSel quickSel = new QuickSel(range_freq.getLeft(), range_freq.getRight());

      for (Assertion a : permanent_assertions) {
        quickSel.addPermanentAssertion(a);
      }

      long time1 = System.nanoTime();
      for (Assertion a : assertions.subList(0, assertionNum)) {
        quickSel.addAssertion(a);
      }
      quickSel.prepareOptimization();
      long time2 = System.nanoTime();

      boolean debug_output = false;
      quickSel.assignOptimalWeights(debug_output);
      long time3 = System.nanoTime();


      for (int i = 0; i < quickSel.weights.size(); i++) {
          if (quickSel.weights.get(i) < -1.5 || quickSel.weights.get(i) > 1.5) {
              System.out.println(i + " " + quickSel.weights.get(i));
          }
      }
      for (Vector<Assertion> queryset : aa) {
        System.out.println("++++++++++++++");
        for (Assertion q : queryset) {
            quickSel.answer(q.query);
          }
          long time4 = System.nanoTime();

          //write time
          System.out.println(String.format("Train time: %.3f, Estimation time: %.3f", (time3 - time1) / 1e9, (time4 - time3) / 1e9));

          //write sel
          double squared_err_sum = 0.0;
          ArrayList<Double> q_list = new ArrayList<Double>();
          for (Assertion q : queryset) {
            Double sel = Math.max(0, quickSel.answer(q.query));
            squared_err_sum += Math.pow(sel - q.freq, 2);
            double q_error = 100000.0;
            if (sel == 0 || q.freq == 0){
              q_error = 1.0;
            } else {
              q_error = Math.max(sel, q.freq) / Math.min(sel, q.freq);
            }
            q_list.add(q_error);
          }
          Collections.sort(q_list);
          for (int pointer : pointers){
            System.out.printf(" %.3f ", q_list.get(pointer - 1));
          }
          double rms_err = Math.sqrt(squared_err_sum / queryset.size());

          System.out.println(String.format("Learning %d assertions, RMS error: %.5f\n", assertionNum, rms_err));

      }

    }
  }

  private static void isomerTest(
      Vector<Assertion> permanent_assertions,
      Vector<Assertion> assertions,
      List<Assertion> queryset) {
    List<Integer> list = Arrays.asList(
        200);
    List<Integer> pointers = Arrays.asList(50,
        95,
        99,
        100);
    for (int assertionNum : list) {
      Pair<Hyperrectangle, Double> range_freq = computeMinMaxRange();
      Isomer isomer = new Isomer(range_freq.getLeft(), range_freq.getRight());

      long time1 = System.nanoTime();
      for (Assertion a : assertions.subList(0, assertionNum)) {
        isomer.addAssertion(a);
      }
      long time2 = System.nanoTime();

      boolean debug_output = false;
      isomer.assignOptimalWeights(debug_output);
      long time3 = System.nanoTime();

      for (Assertion q : queryset) {
        isomer.answer(q.query);
      }
      long time4 = System.nanoTime();

      //write time
      System.out.println(String.format("Insertion time: %.3f, Estimation time: %.3f", (time3 - time1) / 1e9, (time4 - time3) / 1e9));

      //write sel
      double squared_err_sum = 0.0;
      ArrayList<Double> q_list = new ArrayList<Double>();
      for (Assertion q : queryset) {
        Double sel = Math.max(0, isomer.answer(q.query  ));
        squared_err_sum += Math.pow(sel - q.freq, 2);
        double q_error = 100000.0;
        if (sel == 0 || q.freq == 0){
          q_error = 1.0;
        } else {
          q_error = Math.max(sel, q.freq) / Math.min(sel, q.freq);
        }
        q_list.add(q_error);
      }
      Collections.sort(q_list);
      for (int pointer : pointers){
        System.out.printf(" %.3f ", q_list.get(pointer - 1));
      }
      double rms_err = Math.sqrt(squared_err_sum / queryset.size());
      System.out.println(String.format("Learning %d assertions, RMS error: %.5f\n", assertionNum, rms_err));
    }
  }


  private static Pair<Hyperrectangle, Double> computeMinMaxRange() {
    Vector<Pair<Double, Double>> min_max = new Vector<Pair<Double, Double>>();
    min_max.add(Pair.of(0.0, 1.0));
    min_max.add(Pair.of(0.0, 1.0));
//     min_max.add(Pair.of(0.0, 1.0));
//     min_max.add(Pair.of(0.0, 1.0));
//     min_max.add(Pair.of(0.0, 1.0));
//     min_max.add(Pair.of(0.0, 1.0));
//     min_max.add(Pair.of(0.0, 1.0));
//     min_max.add(Pair.of(0.0, 1.0));
//     min_max.add(Pair.of(0.0, 1.0));
//     min_max.add(Pair.of(0.0, 1.0));
    Hyperrectangle min_max_rec = new Hyperrectangle(min_max);
    double total_freq = 1.0;
    return Pair.of(min_max_rec, total_freq);
  }

}



