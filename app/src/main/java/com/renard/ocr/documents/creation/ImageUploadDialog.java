package com.renard.ocr.documents.creation;

import com.android.volley.RetryPolicy;
import com.bumptech.glide.Glide;
import com.bumptech.glide.request.FutureTarget;
import com.bumptech.glide.request.target.SimpleTarget;
import com.bumptech.glide.request.target.Target;
import com.bumptech.glide.request.transition.Transition;
import com.googlecode.leptonica.android.ReadFile;
import com.googlecode.leptonica.android.WriteFile;
import com.googlecode.leptonica.android.Pix;
import com.renard.ocr.R;
import com.renard.ocr.documents.creation.visualisation.OCRActivity;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.util.Base64;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ProgressBar;
import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStream;
import java.util.HashMap;
import java.util.Map;
import java.sql.Timestamp;
import java.lang.Math;
import java.util.concurrent.ExecutionException;

import static java.lang.Thread.sleep;

import static com.renard.ocr.documents.creation.NewDocumentActivity.EXTRA_NATIVE_PIX;
import static com.renard.ocr.documents.creation.NewDocumentActivity.UPLOAD_IMAGE;


/*  Created by: Shreyas Ambekar on
        April 1, 2020
    Modified by Hrishi Budhwant

* */


public class ImageUploadDialog extends Activity {

    public final static String IMAGE_PATH = "image_path";
    int PICK_IMAGE_REQUEST = 111;
    String URLupload = "http://13.233.19.130:80/file-upload";
    ProgressDialog progressDialog;
    Timestamp timestamp = new Timestamp(System.currentTimeMillis());
    final String imgref = new String("IMG" + timestamp.getTime() + (Math.random() * 100));
    boolean download = false;
    private ProgressBar pgsBar;
    private TextView txtview;


    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_imageupload);
        pgsBar = (ProgressBar) findViewById(R.id.pBar);
        txtview = (TextView) findViewById(R.id.text_view_id);
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setMessage("Do you want to upload the image for preprocessing for better accuracy?");
        builder.setTitle("Upload image?");
        builder.setNegativeButton("No", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                Bundle extras = getIntent().getExtras();
                long nativePix = extras.getLong(EXTRA_NATIVE_PIX, 0);
                boolean accessibilityMode = extras.getBoolean(OCRActivity.EXTRA_USE_ACCESSIBILITY_MODE, false);
                Intent result = new Intent();
                result.putExtra(UPLOAD_IMAGE, false);
                result.putExtra(EXTRA_NATIVE_PIX, nativePix);
                result.putExtra(OCRActivity.EXTRA_USE_ACCESSIBILITY_MODE, accessibilityMode);
                setResult(RESULT_OK, result);
                finish();
            }
        });

        builder.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                Bundle extras = getIntent().getExtras();
                long nativePix = extras.getLong(EXTRA_NATIVE_PIX, 0);
                boolean accessibilityMode = extras.getBoolean(OCRActivity.EXTRA_USE_ACCESSIBILITY_MODE, false);
                Pix mpix = new Pix(nativePix);

                Bitmap bitmap = WriteFile.writeBitmap(mpix);


                progressDialog = new ProgressDialog(ImageUploadDialog.this);
                progressDialog.setMessage("Uploading, please wait...");
                progressDialog.show();

                //converting image to base64 string
                ByteArrayOutputStream baos = new ByteArrayOutputStream();
                bitmap.compress(Bitmap.CompressFormat.JPEG, 100, baos);
                byte[] imageBytes = baos.toByteArray();
                final String imageString = Base64.encodeToString(imageBytes, Base64.DEFAULT);
                Timestamp timestamp = new Timestamp(System.currentTimeMillis());
                final String imgref = new String("IMG" + timestamp.getTime() + (Math.random() * 100));

                //sending image to server
                StringRequest request = new StringRequest(Request.Method.POST, URLupload, new Response.Listener<String>() {
                    @SuppressLint("StaticFieldLeak") //Remove this line later
                    @Override
                    public void onResponse(String s) {

                        progressDialog.dismiss();
                        progressDialog.setMessage("Processing Completed - Downloading Image");
                        progressDialog.show();

                        if (s.equals(imgref)) {
                            //final ImageView image = (ImageView) findViewById(R.id.myImageView);
                            Glide.with(ImageUploadDialog.this)
                                    .asBitmap()
                                    .load("http://13.233.19.130:80/static/processed_images/" + imgref + ".jpg")
                                    .into(new SimpleTarget<Bitmap>() {
                                        @Override
                                        public void onResourceReady(Bitmap resource, Transition<? super Bitmap> transition) {
                                            Toast.makeText(ImageUploadDialog.this, "Downloaded Processed Image", Toast.LENGTH_LONG).show();
                                            progressDialog.dismiss();
                                            saveImageCallActivity(resource, imgref, accessibilityMode);
                                        }
                                    });

                        } else {
                            Toast.makeText(ImageUploadDialog.this, "Some error occurred!", Toast.LENGTH_LONG).show();
                            progressDialog.dismiss();
                            finish();
                        }
                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError volleyError) {
                        Toast.makeText(ImageUploadDialog.this, "Some error occurred -> " + volleyError, Toast.LENGTH_LONG).show();
                        progressDialog.dismiss();
                        finish();
                    }
                }) {
                    //adding parameters to send
                    protected Map<String, String> getParams() throws AuthFailureError {
                        Map<String, String> parameters = new HashMap<String, String>();
                        //parameters.put("image", imageString);
                        parameters.put("image", imageString);
                        parameters.put("filename", imgref);
                        return parameters;
                    }
                };

                request.setRetryPolicy(new RetryPolicy() {
                    @Override
                    public int getCurrentTimeout() {
                        return 600000;
                    }

                    @Override
                    public int getCurrentRetryCount() {
                        return 600000;
                    }

                    @Override
                    public void retry(VolleyError error) throws VolleyError {

                    }
                });
                RequestQueue rQueue = Volley.newRequestQueue(ImageUploadDialog.this);
                rQueue.add(request);
            }
        });
        AlertDialog alert = builder.create();
        alert.setCanceledOnTouchOutside(false);
        alert.show();
    }

    private void saveImageCallActivity(Bitmap image, String imgref, Boolean accessibilityMode) {

        String savedImagePath = null;

        String imageFileName = imgref + ".jpg";
        File storageDir = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS)
                + "/Textdroid");
        boolean success = true;
        if (!storageDir.exists()) {
            success = storageDir.mkdirs();
        }
        if (success) {
            File imageFile = new File(storageDir, imageFileName);
            savedImagePath = imageFile.getAbsolutePath();
            try {
                OutputStream fOut = new FileOutputStream(imageFile);
                image.compress(Bitmap.CompressFormat.JPEG, 100, fOut);
                fOut.close();
            } catch (Exception e) {
                e.printStackTrace();
            }

            // Add the image to the system gallery
            galleryAddPic(savedImagePath);
        }
        Intent result = new Intent();
        result.putExtra(UPLOAD_IMAGE, true);
        result.putExtra(IMAGE_PATH, savedImagePath);
        result.putExtra(OCRActivity.EXTRA_USE_ACCESSIBILITY_MODE, accessibilityMode);
        setResult(RESULT_OK, result);
        finish();

    }

    private void galleryAddPic(String imagePath) {
        Intent mediaScanIntent = new Intent(Intent.ACTION_MEDIA_SCANNER_SCAN_FILE);
        File f = new File(imagePath);
        Uri contentUri = Uri.fromFile(f);
        mediaScanIntent.setData(contentUri);
        sendBroadcast(mediaScanIntent);
    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();
        setResult(RESULT_CANCELED);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
    }

}

