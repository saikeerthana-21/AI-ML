// Source code is decompiled from a .class file using FernFlower decompiler (from Intellij IDEA).
public class SmartLockPin {
   public SmartLockPin() {
   }

   static boolean test(int var0) {
      int var1 = var0;
      int var2 = 0;

      for(int var3 = 0; var3 < 4; ++var3) {
         int var4 = var1 % 10;
         if (var4 % 2 != 0) {
            return false;
         }

         var2 += var4;
         var1 /= 10;
      }

      return var2 == 16;
   }

   public static void main(String[] var0) {
      System.out.println("Possible PINs:");

      for(int var1 = 0; var1 <= 9999; ++var1) {
         if (test(var1)) {
            System.out.printf("%04d\n", var1);
         }
      }

   }
}