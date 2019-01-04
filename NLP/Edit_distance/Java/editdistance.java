import java.io.*;
import java.util.*;

class editdistance{
    public static int INFINITY = 30;//The longest word in the corpus is 24 characters long

    public static int subs_cost(char ch1,char ch2) {
        if (ch1 == ch2)
            return 0;
        return 1;
    }

    public static boolean min_bounds_check(int i,int j,int min_edits) {
        if (i > min_edits && j >  min_edits)
            return true;
        return false;
    }

    public static int levenstein(String source, String dest) {
        int N = dest.length();
        int M = source.length();
        int i,j;

        int[][] distance = new int[N+1][M+1];
        for (int[] row:distance) {
            Arrays.fill(row,INFINITY);
        }
        distance[0][0] = 0;
        for (i = 1; i < N+1; i++ )
            distance[i][0] = distance[i-1][0] + 1; //insertion cost of dest[i-1]

        for (j = 1; j < M+1; j++ )
            distance[0][j] = distance[0][j-1] + 1; //deletion cost of source[j-1]

        for (i = 1; i < N+1; i++ ) {
            for (j = 1; j < M+1; j++ ) {
                distance[i][j] = Math.min(distance[i-1][j] + 1,
                                          Math.min(distance[i][j-1] + 1 ,
                                                   distance[i-1][j-1] + subs_cost(source.charAt(j-1),dest.charAt(i-1))));
            }
            /*
            if ( min_bounds_check(i,j-1,min_edits) && distance[i][j-1] > min_edits) {
                return INFINITY;
            }*/
        }
        return distance[N][M];
    }

    public static boolean is_swap_possible(String a,String b,int i,int j){
            return (a.charAt(j) == b.charAt(i-1) && a.charAt(j-1) == b.charAt(i));
    }

    public static int osa(String source, String dest) {
        int N = dest.length();
        int M = source.length();
        int i,j;

        int[][] distance = new int[N+1][M+1];
        for (int[] row:distance) {
            Arrays.fill(row,INFINITY);
        }
        distance[0][0] = 0;
        for (i = 1; i < N+1; i++ )
            distance[i][0] = distance[i-1][0] + 1; //insertion cost of dest[i-1]

        for (j = 1; j < M+1; j++ )
            distance[0][j] = distance[0][j-1] + 1; //deletion cost of source[j-1]

        for (i = 1; i < N+1; i++ ) {
            for (j = 1; j < M+1; j++ ) {
                distance[i][j] = Math.min(distance[i-1][j] + 1,
                                          Math.min(distance[i][j-1] + 1 ,
                                                   distance[i-1][j-1] + subs_cost(source.charAt(j-1),dest.charAt(i-1))));
                if (i > 1 && j > 1 && is_swap_possible(source,dest,i-1,j-1))
                    distance[i][j] = Math.min(distance[i][j],distance[i-2][j-2]+1);
            }
            /*
            if ( min_bounds_check(i,j-1,min_edits) && distance[i][j-1] > min_edits) {
                return INFINITY;
            }*/
        }
        return distance[N][M];
    }

    public static int Damerau_Levenstein(String source,String dest) {
        int len_alpha = 26;
        int[] da = new int[len_alpha];
        int db;
        int i,j,k,l,cost;
        int N = dest.length();
        int M = source.length();

        for (i = 0; i < len_alpha; i++)
            da[i] = 0;

        int[][] distance = new int[M+2][N+2];
        for (int[] row:distance) {
            Arrays.fill(row,INFINITY);
        }
        int maxdist = N+M;
        distance[0][0] = maxdist;

        for (i = 1; i < M+2; i++ ) {
            distance[i][0] = maxdist;
            distance[i][1] = i; 
        }

        for (j = 1; j < N+2; j++ ) {
            distance[0][j] = maxdist;
            distance[1][j] = j; 
        }

        for (i = 2; i < M+2; i++ ) {
            db = 1;
            for (j = 2; j < N+2; j++ ) {
                k = da[dest.charAt(j-2)-'a'];
                l = db;
                if (source.charAt(i-2) == dest.charAt(j-2)) {
                    cost = 0;
                    db = j-2;
                } else {
                    cost = 1;
                }
                distance[i][j] = Math.min(distance[i-1][j-1] + cost,
                                              Math.min(distance[i][j-1] +1,
                                                       Math.min(distance[i-1][j] + 1,
                                                                distance[k][l]   + ((i)-(k)-(l)) + 1 + ((j)-(l)-1) )));
            }
            da[source.charAt(i-2)-'a'] = i-2;
        }
        return distance[M+1][N+1];
            
    }
     

    public static void main(String args[]) throws IOException{
        int LEVENSTEIN = 1;
        int OSA = 2;
        int DL = 3;
        int TRIE = 4;

        int mode = Integer.parseInt(args[0]);
        String input_file = args[1];
        String dict_file = args[2];
        String output_file = args[3];

        Scanner in = new Scanner(new File(input_file));
        Scanner dictionary = new Scanner(new File(dict_file));
        PrintWriter out = new PrintWriter(output_file);

        ArrayList<String> raw = new ArrayList<String>();
        ArrayList<String> dict = new ArrayList<String>();
        ArrayList<String> sorted_dict = new ArrayList<String>();

        int i = 0;
        while(in.hasNextLine()) {
            raw.add(in.nextLine());
        }

        while(dictionary.hasNextLine()) {
            dict.add(dictionary.nextLine());
        }

        Collections.sort(dict, Comparator.comparing(String::length));

        /*
        int somedist = levenstein("college","ocllege");
        System.out.println("levenstein:"+somedist);
        
        somedist = osa("college","ocllege");
        System.out.println("osa:"+somedist);

        somedist = Damerau_Levenstein("ca","abc");
        System.out.println("Damerau levenstein:"+somedist);
        */

        for (String word:raw) {
            boolean correct = dict.contains(word);
            //System.out.println(correct);
            if (correct) {
                out.write(word+" "+String.valueOf(0)+"\n");
            }
            else {
                int wlen = word.length();
                int min_edits = wlen;

                String target_candidate = null;
                for(String target:dict) {
                    int dist = min_edits;
                    int tlen = target.length();

                    /*
                    if (tlen - wlen > min_edits || wlen - tlen > min_edits) {
                        continue;
                    } else {*/ 
                    if (LEVENSTEIN == mode) {
                        dist = levenstein(word,target);
                    } else if (OSA == mode) {
                        dist = osa(word,target);
                    } else if (DL == mode) {
                        dist = Damerau_Levenstein(word,target);
                    }
                    if (min_edits > dist) {
                        min_edits = dist;
                        target_candidate = target;
                        if (1 == min_edits)
                            break;
                    }                    
                }
                out.write(target_candidate+" "+String.valueOf(min_edits)+"\n");
            }
        }
        in.close();
        dictionary.close();
        out.close();
    }
}
